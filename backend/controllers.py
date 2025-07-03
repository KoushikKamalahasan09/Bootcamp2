from flask_restful import Resource, Api
from flask import request

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
        users = User.query.all()
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
            return {'msg': "User already exists!"}, 400
        user = User(email=email, username=username, passhash=passhash, is_admin=False)
        db.session.add(user); db.session.commit()
        return {'msg': "Successfully created user!"}
    
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
        if 'email' in data:
            if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
                return {'msg': "Email already exists!"}, 400
            user.email = data['email']
        if 'username' in data:
            if User.query.filter_by(username=data['username']).first() and data['username'] != user.username:
                return {'msg': "Username already exists!"}, 400
            user.username = data['username']
        
        db.session.commit()
        return {
            'msg': "User information updated!",
            'user': {
                'Username': user.username,
                'email': user.email,
                'Admin?': user.is_admin
            }
        }, 200

    
    def delete(self, user_id=None):
        if not user_id:
            return {'msg': "User email is required to delete!"}, 400
        user = User.query.get(user_id)
        if not user:
            return {'msg': "User not exists to delete!"}, 404
        db.session.delete(user)
        db.session.commit()
        return {'msg': "User has been delete!"}, 200
    
class Parkinglots(Resource):
    
    
    def get(self,lot_id=None):
        if lot_id:
            lot = ParkingLot.query.get(lot_id)
            if lot:
                return {'msg': "Lot found", 'Location': lot.location_name, 'Price per Hour': lot.price_per_hour, 'Address': lot.address, 'Pin Code': lot.pin_code, 'Number of Spots': lot.number_of_spots}
            return {'msg': "User not found!"}, 404
        lots = ParkingLot.query.all()
        lots = [{'Location': lot.location_name, 'Price per Hour': lot.price_per_hour, 'Address': lot.address, 'Pin Code': lot.pin_code, 'Number of Spots': lot.number_of_spots} for lot in lots]
        return {"msg": "All parking lots", "lots": lots}
    
    def post(self):
        data = request.get_json()
        location_name = data.get('location_name', None)
        price_per_hour = data.get('price_per_hour', None)
        address = data.get('address', None)
        pin_code = data.get('pin_code', None)
        number_of_spots = data.get('number_of_spots', None)
        
        if not location_name or not price_per_hour or not address or not pin_code or not number_of_spots:
            return {'msg': "Please provide all required information!"}, 400
        
        lot = ParkingLot(location_name=location_name, price_per_hour=price_per_hour, address=address, pin_code=pin_code, number_of_spots=number_of_spots)
        db.session.add(lot); db.session.commit()
        return {'msg': "Successfully created parking lot!"}
    
    def put(self, lot_id=None):
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

        return {
            'msg': "Parking lot information updated!",
            'lot': {
                'Location': lot.location_name,
                'Price per Hour': lot.price_per_hour,
                'Address': lot.address,
                'Pin Code': lot.pin_code,
                'Number of Spots': lot.number_of_spots
            }
        }, 200
        
    def delete(self, lot_id=None):
        if not lot_id:
            return {'msg': "Parking lot ID is required to delete!"}, 400
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': "Parking lot does not exist!"}, 404
        db.session.delete(lot)
        db.session.commit()
        return {'msg': "Parking lot has been deleted!"}, 200
    
class ParkingSpots(Resource):
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if spot:
                return {
                    'msg': "Spot found",
                    'Spot Number': spot.spot_number,
                    'Available?': spot.is_avail,
                    'Lot ID': spot.lot_id
                }
            return {'msg': "Spot not found"}, 404

        spots = ParkingSpot.query.all()
        result = [{
            'Spot Number': s.spot_number,
            'Available?': s.is_avail,
            'Lot ID': s.lot_id
        } for s in spots]
        return {'msg': "All spots", 'spots': result}, 200

    def post(self):
        data = request.get_json()
        lot_id = data.get('lot_id')
        spot_number = data.get('spot_number')
        if not lot_id or not spot_number:
            return {'msg': "Missing spot number or lot ID"}, 400

        spot = ParkingSpot(lot_id=lot_id, spot_number=spot_number)
        db.session.add(spot)
        db.session.commit()
        return {'msg': "Parking spot created!"}, 201

    def put(self, spot_id=None):
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

    def delete(self, spot_id=None):
        if not spot_id:
            return {'msg': "Spot ID required"}, 400
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': "Spot not found"}, 404

        db.session.delete(spot)
        db.session.commit()
        return {'msg': "Spot deleted!"}, 200

class Reservations(Resource):
    def get(self, reservation_id=None):
        if reservation_id:
            r = Reservation.query.get(reservation_id)
            if not r:
                return {'msg': "Reservation not found"}, 404
            cost="In Progress" if r.leaving_timestamp is None else r.spot.lot.price_per_hour * round((r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600, 2)
            return {
                'msg': "Reservation found",
                'User ID': r.user_id,
                'Spot ID': r.spot_id,
                'From': str(r.parking_timestamp),
                'To': str(r.leaving_timestamp),
                'Cost': cost,
                'Active?': r.is_active
            }

        reservations = Reservation.query.all()
        data = [{
            'Username': r.user.username,
            'Spot ID': r.spot_id,
            'From': str(r.parking_timestamp),
            'To': str(r.leaving_timestamp),
            'Active?': r.is_active
        } for r in reservations]
        return {'msg': "All reservations", 'reservations': data}

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

    def put(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID is required"}, 400
        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404

        data = request.get_json()
        if 'leaving_timestamp' in data:
            r.leaving_timestamp = data['leaving_timestamp']
        if 'parking_cost' in data:
            r.parking_cost = data['parking_cost']
        if 'is_active' in data:
            r.is_active = data['is_active']

        db.session.commit()
        return {'msg': "Reservation updated!"}, 200

    def delete(self, reservation_id=None):
        if not reservation_id:
            return {'msg': "Reservation ID required"}, 400
        r = Reservation.query.get(reservation_id)
        if not r:
            return {'msg': "Reservation not found"}, 404
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
        return {"msg": "Login successful",'token': token}, 200
        
        