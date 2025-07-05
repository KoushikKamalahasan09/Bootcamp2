from flask_restful import Resource, Api
from flask import request
from datetime import datetime

from models import db, User,ParkingLot, ParkingSpot, Reservation
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token

class UsersResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {'msg': "user found", 'user': user.to_dict()}
            return {'msg': "User not found!"}, 404
        users = [user.to_dict() for user in User.query.all()]
        return {"msg": "All users", "users": users}
    
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
        return {'msg': "Successfully created user!"}
    
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
        return {'msg': "User has been delete!"}, 200
    
class Parkinglots(Resource):
    
    @jwt_required()
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
            lot.number_of_spots = data['number_of_spots']

        db.session.commit()
        lot=ParkingLot.query.get(lot_id)

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
        return {'msg': "Parking lot has been deleted!"}, 200
    
class ParkingSpots(Resource):
    
    @jwt_required()
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if spot:
                return {'msg': "Spot found",'spot': spot.to_dict()}
            return {'msg': "Spot not found"}, 404
        
        lot_id=request.args.get('lot_id')
        if lot_id:
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
            return {'msg': "Spots in lot", 'spots': [spot.to_dict() for spot in spots]}, 200

        spots = [spot.to_dict() for spot in ParkingSpot.query.all()]
        return {'msg': "All spots", 'spots': spots}, 200

    @jwt_required()
    def post(self):
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to create parking spots!"}, 403
        data = request.get_json()
        lot_id = data.get('lot_id')
        spot_number = data.get('spot_number')
        if not lot_id or not spot_number:
            return {'msg': "Missing spot number or lot ID"}, 400

        spot = ParkingSpot(lot_id=lot_id, spot_number=spot_number)
        db.session.add(spot)
        db.session.commit()
        return {'msg': "Parking spot created!"}, 201

    @jwt_required()
    def put(self, spot_id=None):
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to update parking spots!"}, 403
        if not spot_id:
            return {'msg': "Spot ID required"}, 400
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Spot not found"}, 404

        data = request.get_json()
        if 'is_avail' in data:
            spot.is_avail = data['is_avail']
        if 'spot_number' in data:
            spot.spot_number = data['spot_number']
        if 'lot_id' in data:
            spot.lot_id = data['lot_id']

        db.session.commit()
        return {'msg': "Spot updated!"}, 200

    @jwt_required()
    def delete(self, spot_id=None):
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin:
            return {'msg': "You are not authorized to delete parking spots!"}, 403
        if not spot_id:
            return {'msg': "Spot ID required"}, 400
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Spot not found"}, 404

        db.session.delete(spot)
        db.session.commit()
        return {'msg': "Spot deleted!"}, 200

class Reservations(Resource):
    
    @jwt_required()
    def get(self, reservation_id=None):
        if reservation_id:
            r = Reservation.query.get(reservation_id)
            if not r:
                return {'msg': "Reservation not found"}, 404
            id=get_jwt_identity()
            user=User.query.get(id)
            if not user.is_admin and r.user_id != id:
                return {'msg': "You are not authorized to view this reservation"}, 403
            cost=r.spot.lot.price_per_hour*round((datetime.now()-r.parking_timestamp).total_seconds()/3600,2) if r.leaving_timestamp is None else r.spot.lot.price_per_hour * round((r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600, 2)
            r.cost=cost
            db.session.commit()
            
            return {'msg': "Reservation found",'Spor Details': r.spot.to_dict(), 'User Details': r.user.to_dict()},200


        reservations = Reservation.query.all()
        return {'msg': "All reservations", 'reservations': [r.to_dict() for r in reservations]}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        spot_id = data.get('spot_id')
        leaving_timestamp = data.get('leaving_timestamp')

        if not user_id or not spot_id:
            return {'msg': "Missing user_id or spot_id"}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot or not spot.is_avail:
            return {'msg': "Spot not available"}, 400

        reservation = Reservation(
            user_id=user_id,
            spot_id=spot_id,
            leaving_timestamp=leaving_timestamp,
            parking_cost=0.0  # you can calculate based on duration
        )
        spot.is_avail = False  # mark as unavailable

        db.session.add(reservation)
        db.session.commit()
        return {'msg': "Reservation created!"}, 201

    
    @jwt_required()
    def put(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID is required"}, 400
        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404
        
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin and r.user_id != id:
            return {'msg': "You are not authorized to view this reservation"}, 403

        data = request.get_json()
        if 'leaving_timestamp' in data:
            r.leaving_timestamp = data['leaving_timestamp']
        if 'parking_cost' in data:
            r.parking_cost = data['parking_cost']
        if 'is_active' in data:
            r.is_active = data['is_active']

        db.session.commit()
        return {'msg': "Reservation updated!"}, 200

    @jwt_required()
    def delete(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID required"}, 400
        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404
        
        id=get_jwt_identity()
        user=User.query.get(id)
        if not user.is_admin and r.user_id != id:
            return {'msg': "You are not authorized to view this reservation"}, 403
        db.session.delete(r)
        db.session.commit()
        return {'msg': "Reservation deleted!"}, 200


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