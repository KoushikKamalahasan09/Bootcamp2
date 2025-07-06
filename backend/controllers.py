from flask_restful import Resource, Api
from flask import request
from datetime import datetime
#from time import sleep


from models import db, User,ParkingLot, ParkingSpot, Reservation
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from flask_caching import Cache

cache=Cache()

class UsersResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {'msg': "user found", 'user': user.to_dict()}
            return {'msg': "User not found!"}, 404
        return self._get_all_users()
    
    @cache.cached(timeout=600, key_prefix='users_list')
    def _get_all_users(self):
        users = [user.to_dict() for user in User.query.all()]
        return {"msg": "All users", "users": users}, 200
    
    def post(self):
        data = request.get_json()
        username = data.get('username', None)
        email = data.get('email', None)
        passhash = data.get('password', None)
        if not email or not username or not passhash:
            return {'msg': "Please provide all required information!"}, 400
        user = User.query.filter_by(email=email).first()
        if user:
            return {'msg': "User already exists!"}, 409
        user = User(email=email, username=username, passhash=passhash, is_admin=False)
        db.session.add(user); db.session.commit()
        cache.delete('users_list')  # Clear cache after adding a new user
        return {'msg': "Successfully created user!"}
    
    @jwt_required()
    def _get_user_count(self):
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            return {'msg': 'Unauthorized'}, 403

        count = User.query.count()
        return {'total_users': count}
    
    @jwt_required()
    def put(self, user_id=None):
        if not user_id:
            return {'msg': "User id is required to update!"}, 400
        user = User.query.get(user_id)
        if not user:
            return {'msg': "User not exists to update!"}, 404
        data = request.get_json()
        if not data:
            return {'msg': "No data provided for update!"}, 400
        
        

        # Update only the fields that are present in the request
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return {'msg': "Email already exists!"}, 400
            user.email = data['email']
        
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return {'msg': "Username already exists!"}, 400
            user.username = data['username']

        
        db.session.commit()
        users = user.to_dict()
        cache.delete('users_list')  # Clear cache after updating user information
        return {"msg": "User Information updated", "user": users},200


    @jwt_required()
    def delete(self, user_id=None):
        if not user_id:
            return {'msg': "User id is required to delete!"}, 400
        user = User.query.get(user_id)
        if not user:
            return {'msg': "User not exists to delete!"}, 404
        if user.is_admin:
            return {'msg': "You cannot delete an admin user!"}, 403
        db.session.delete(user)
        db.session.commit()
        cache.delete('users_list')  # Clear cache after deleting a user
        return {'msg': "User has been delete!"}, 200
    
class Parkinglots(Resource):
    
    @jwt_required()
    @cache.cached(timeout=600,key_prefix='parking_lots_list')
    def get(self,lot_id=None):
        if lot_id:
            lot = ParkingLot.query.get(lot_id)
            if lot:
                return {'msg': "Lot found", 'Lot': lot.to_dict()}
            return {'msg': "Lot not found!"}, 404
        lots = [lot.to_dict() for lot in ParkingLot.query.all()]
        if not lots:
            return {'msg': "No parking lots available!"}, 200
        return {"msg": "All parking lots", "lots": lots},200
    
    @jwt_required()
    def post(self):
        id=get_jwt_identity()
        print(id)
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to create parking lots!"}, 403
        data = request.get_json()
        location_name = data.get('location_name', None)
        price_per_hour = data.get('price_per_hour', None)
        address = data.get('address', None)
        pin_code = data.get('pincode', None)
        number_of_spots = data.get('number_of_spots', None)
        
        if not location_name or not price_per_hour or not address or not pin_code or not number_of_spots:
            return {'msg': "Please provide all required information!"}, 400
        
        lot = ParkingLot(location_name=location_name, price_per_hour=price_per_hour, address=address, pin_code=pin_code, number_of_spots=number_of_spots)
        db.session.add(lot); db.session.commit()
        
        for i in range(1, number_of_spots + 1):
            spot=ParkingSpot(lot_id=lot.id, spot_number=i, is_avail=True)
            db.session.add(spot)
        db.session.commit()
        cache.delete('parking_lots_list')  # Clear cache after adding a new parking lot
        
        return {'msg': "Successfully created parking lot!"}
    
    @jwt_required()
    def put(self, lot_id=None):
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to update parking lots!"}, 403
        if not lot_id:
            return {'msg': "Parking lot ID is required to update!"}, 400
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': "Parking lot does not exist!"}, 404
        data = request.get_json()
        
        if not data:
            return {'msg': "No data provided for update!"}, 400

        # Update only the fields that are present in the request
        if 'location_name' in data:
            lot.location_name = data['location_name']
        if 'price_per_hour' in data:
            lot.price_per_hour = data['price_per_hour']
        if 'address' in data:
            lot.address = data['address']
        if 'pin_code' in data:
            lot.pin_code = data['pin_code']
        if 'number_of_spots' in data:
            current_spots = ParkingSpot.query.filter_by(lot_id=lot_id).count()
            new_spots = data['number_of_spots']

            if new_spots > current_spots:
                for i in range(current_spots + 1, new_spots + 1):
                    spot = ParkingSpot(lot_id=lot.id, spot_number=i, is_avail=True)
                    db.session.add(spot)
            elif new_spots < current_spots:
                # Delete the most recent (likely unused) spots
                excess_spots = (
                    ParkingSpot.query
                    .filter_by(lot_id=lot_id)
                    .order_by(ParkingSpot.id.desc())  # using spot.id as it's guaranteed to be unique
                    .limit(current_spots - new_spots)
                    .all()
                )
                for spot in excess_spots:
                    db.session.delete(spot)

            # Now finally update the field
            lot.number_of_spots = new_spots
        db.session.commit()
        lot=ParkingLot.query.get(lot_id)
        cache.delete('parking_lots_list')  # Clear cache after updating parking lot information
        

        return {"msg": "Updated parking lot Information", "Lot": lot.to_dict()}, 200
        
    @jwt_required()
    def delete(self, lot_id=None):
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to delete parking lots!"}, 403
        if not lot_id:
            return {'msg': "Parking lot ID is required to delete!"}, 400
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': "Parking lot does not exist!"}, 404
        db.session.delete(lot)
        db.session.commit()
        cache.delete('parking_lots_list')  # Clear cache after deleting parking lot
        cache.delete('parking_spots')  # Clear cache for parking spots as well
        return {'msg': "Parking lot has been deleted!"}, 200
    

class ParkingSpots(Resource):

    @jwt_required()
    
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if not spot:
                return {'msg': "Spot not found"}, 404
            return {'msg': "Spot found", 'spot': spot.to_dict()}, 200

        lot_id = request.args.get('lot_id')

        # Optional: Time-based availability query
        start = request.args.get('start')
        end = request.args.get('end')

        query = ParkingSpot.query
        if lot_id:
            query = query.filter_by(lot_id=lot_id)

        spots = query.all()
        result = []

        if start and end:
            try:
                start_time = datetime.fromisoformat(start)
                end_time = datetime.fromisoformat(end)
            except ValueError:
                return {'msg': 'Invalid timestamp format. Use ISO 8601 format.'}, 400

            for spot in spots:
                overlapping = Reservation.query.filter(
                    Reservation.spot_id == spot.id,
                    Reservation.is_active == True,
                    Reservation.parking_timestamp < end_time,
                    Reservation.leaving_timestamp > start_time
                ).first()
                if not overlapping:
                    result.append(spot.to_dict())
            return {'msg': f"Available spots in time range", 'spots': result}, 200

        # No time filter, return all spots
        now = datetime.now()
        result = []

        for spot in spots:
            spot_data = spot.to_dict()

            active_res = Reservation.query.filter(
                Reservation.spot_id == spot.id,
                Reservation.is_active == True,
                Reservation.parking_timestamp <= now,
                Reservation.leaving_timestamp >= now
            ).all()

            if active_res:
                spot_data['reservation'] =[ {
                    'user_id': r.user_id,
                    'username': r.user.username,
                    'start_time': r.parking_timestamp.isoformat(),
                    'end_time': r.leaving_timestamp.isoformat()
                }for r in active_res]
            else:
                spot_data['reservation'] = None

            result.append(spot_data)

        return {'msg': "All spots", 'spots': result}, 200


    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return {'msg': "You are not authorized to create parking spots!"}, 403

        data = request.get_json()
        lot_id = data.get('lot_id')
        spot_number = data.get('spot_number')

        if not lot_id or not spot_number:
            return {'msg': "Missing lot_id or spot_number"}, 400

        # Optional: prevent duplicate spot numbers in same lot
        exists = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if exists:
            return {'msg': "Spot number already exists in this lot"}, 409

        spot = ParkingSpot(lot_id=lot_id, spot_number=spot_number)
        db.session.add(spot)
        db.session.commit()
        

        return {'msg': "Parking spot created", 'spot_id': spot.id}, 201

    @jwt_required()
    def put(self, spot_id=None):
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return {'msg': "You are not authorized to update parking spots!"}, 403

        if not spot_id:
            return {'msg': "Spot ID is required"}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Spot not found"}, 404

        data = request.get_json()
        if 'spot_number' in data:
            spot.spot_number = data['spot_number']
        if 'lot_id' in data:
            spot.lot_id = data['lot_id']

        db.session.commit()
        
        return {'msg': "Spot updated"}, 200

    @jwt_required()
    def delete(self, spot_id=None):
        id = get_jwt_identity()
        user = User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to delete parking spots!"}, 403
        if not spot_id:
            return {'msg': "Spot ID required"}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Spot not found"}, 404

        # Save info before deleting
        lot_id = spot.lot_id
        spot_number = spot.spot_number

        # Delete the spot
        db.session.delete(spot)
        db.session.commit()

        # Re-create a fresh spot with same lot_id and spot_number
        new_spot = ParkingSpot(lot_id=lot_id, spot_number=spot_number)
        db.session.add(new_spot)
        db.session.commit()
        

        return {
            'msg': f"Spot {spot_number} deleted and re-created successfully!",
            'new_spot': new_spot.to_dict()
        }, 200


class Reservations(Resource):
    
    @jwt_required()
    def get(self, reservation_id=None):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if reservation_id:
            r = Reservation.query.get(reservation_id)
            if not r:
                return {'msg': "Reservation not found"}, 404
            if not (user.is_admin or r.user_id == int(user_id)):
                return {'msg': "You are not authorized to view this reservation"}, 403
            return {
                'msg': "Reservation found",
                'reservation': r.to_dict(),
                'spot': r.spot.to_dict(),
                'user': r.user.to_dict()
            }, 200

        # Admins get all, users get their own
        if user.is_admin:
            reservations = Reservation.query.all()
        else:
            reservations = Reservation.query.filter_by(user_id=user_id).all()

        return {
            'msg': "Reservations retrieved",
            'reservations': [r.to_dict() for r in reservations]
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        spot_id = data.get('spot_id')
        start_raw = data.get('parking_timestamp')
        end_raw = data.get('leaving_timestamp')

        if not spot_id or not start_raw or not end_raw:
            return {'msg': "spot_id, parking_timestamp, and leaving_timestamp are required"}, 400

        try:
            start_time = datetime.fromisoformat(start_raw)
            end_time = datetime.fromisoformat(end_raw)
        except ValueError:
            return {'msg': 'Invalid timestamp format. Use ISO format.'}, 400

        if start_time >= end_time:
            return {'msg': 'Start time must be before end time'}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Parking spot not found"}, 404

        # Overlapping check
        overlapping = Reservation.query.filter(
            Reservation.spot_id == spot_id,
            Reservation.is_active == True,
            Reservation.parking_timestamp < end_time,
            Reservation.leaving_timestamp > start_time
        ).first()

        if overlapping:
            return {'msg': "Spot already reserved during this time"}, 409

        reservation = Reservation(
            user_id=user_id,
            spot_id=spot_id,
            parking_timestamp=start_time,
            leaving_timestamp=end_time,
            is_active=True
        )
        db.session.add(reservation)
        db.session.commit()

        return {'msg': "Reservation created successfully", 'reservation_id': reservation.id}, 201

    @jwt_required()
    def put(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID is required"}, 400

        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        # ✅ Fixed authorization check: allow admin OR user owning the reservation
        if not (user.is_admin or r.user_id == int(user_id)):
            return {'msg': "You are not authorized to modify this reservation"}, 403

        data = request.get_json()

        # Parse and validate timestamps
        new_start = r.parking_timestamp
        new_end = r.leaving_timestamp

        if 'parking_timestamp' in data:
            try:
                new_start = datetime.fromisoformat(data['parking_timestamp'])
            except ValueError:
                return {'msg': "Invalid parking_timestamp format"}, 400

        if 'leaving_timestamp' in data:
            try:
                new_end = datetime.fromisoformat(data['leaving_timestamp'])
            except ValueError:
                return {'msg': "Invalid leaving_timestamp format"}, 400

        if new_start >= new_end:
            return {'msg': "Start time must be before end time"}, 400

        # ✅ Overlap check (excluding current reservation)
        overlapping = Reservation.query.filter(
            Reservation.spot_id == r.spot_id,
            Reservation.id != r.id,  # Exclude self
            Reservation.is_active == True,
            Reservation.parking_timestamp < new_end,
            Reservation.leaving_timestamp > new_start
        ).first()

        if overlapping:
            return {'msg': "This spot is already reserved during that time."}, 409

        # Save updated times
        r.parking_timestamp = new_start
        r.leaving_timestamp = new_end

        # Optional: toggle status if provided
        if 'is_active' in data:
            r.is_active = data['is_active']

        db.session.commit()
        return {'msg': "Reservation updated successfully"}, 200


    @jwt_required()
    def delete(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID required"}, 400

        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        print(f"Logged in user_id: {user_id}, Reservation user_id: {r.user_id}")


        # 🔒 Permission check (same as put)
        if not (user.is_admin or r.user_id == int(user_id)):
            return {'msg': "You are not authorized to delete this reservation"}, 403

        now = datetime.now()

        # 🔁 If the reservation has already started, don't delete — just update end time
        if r.parking_timestamp <= now:
            r.leaving_timestamp = now
            r.is_active = False
            db.session.commit()
            return {'msg': "Reservation shortened to end now (cannot delete past reservations)"}, 200

        # 🗑 If the reservation is in the future, safe to delete
        db.session.delete(r)
        db.session.commit()
        return {'msg': "Reservation deleted successfully"}, 200

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'msg': "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'msg': "User not found"}, 404
        if user.passhash != password:
            return {'msg': "Invalid password"}, 401
        token=create_access_token(identity=str(user.id))
        return {"msg": "Login successful",'token': token,"user_id":user.id,"isadmin":user.is_admin}, 200
        


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        if not email or not username or not password:
            return {'msg': "Please provide all required information!"}, 400
        user = User.query.filter_by(email=email).first()
        if user:
            return {'msg': "User already exists!"}, 409
        user = User(email=email, username=username, passhash=password)
        db.session.add(user); db.session.commit()
        return {'msg': "Successfully Registered!"}, 200     