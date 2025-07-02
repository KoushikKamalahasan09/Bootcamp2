from flask_restful import Resource, Api
from flask import request

from models import db, User,ParkingLot#, ParkingSpot, Reservation

'''class UsersResource(Resource):
    
    def get(self, user_id=None):
        if user_id:
            user = Users.query.get(user_id)
            if user:
                return {'msg': "user found", 'email': user.email, 'name': user.name}
            return {'msg': "User not found!"}, 404
        users = Users.query.all()
        users = [{'email': user.email, 'name': user.name} for user in users]
        return {"msg": "All users", "users": users}
    
    def post(self):
        data = request.get_json()
        email = data.get('email', None)
        name = data.get('name', None)
        if not email or not name:
            return {'msg': "Please provide all required information!"}, 400
        user = Users.query.get(email)
        if user:
            return {'msg': "User already exists!"}, 400
        user = Users(email=email, name=name)
        db.session.add(user); db.session.commit()
        return {'msg': "Successfully created user!"}
    
    def put(self, user_id=None):
        if not user_id:
            return {'msg': "User email is required to update!"}, 400
        user = Users.query.get(user_id)
        if not user:
            return {'msg': "User not exists to update!"}, 404
        data = request.get_json()
        name = data.get('name', None)
        if not name:
            return {'msg': "Please provide all required information!"}, 400
        user.name = name
        db.session.commit()
        user = {'email': user.email, 'name': user.name}
        return {'msg': "User information updated!", 'user': user}, 200
    
    def delete(self, user_id=None):
        if not user_id:
            return {'msg': "User email is required to delete!"}, 400
        user = Users.query.get(user_id)
        if not user:
            return {'msg': "User not exists to delete!"}, 404
        db.session.delete(user)
        db.session.commit()
        return {'msg': "User has been delete!"}, 200'''
    
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