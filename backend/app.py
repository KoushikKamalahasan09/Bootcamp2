from flask import Flask, render_template, request
from flask_cors import CORS
from models import db,User,ParkingLot,ParkingSpot,Reservation
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from controllers import Parkinglots,UsersResource,ParkingSpots,Reservations,LoginResource,RegisterResource,cache

# backend/app.py


app = Flask(__name__)
api = Api(app)

CORS(app)

# connecting database




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'c5faf247641cfc78c25d4b2ccd1bb07d079cbe3a31310aed98cbb4c62b4cc003'

jwt=JWTManager(app)

# initializing database
db.init_app(app)

# connecting api resources to endpoints


api.add_resource(Parkinglots, '/lots', '/lots/<lot_id>')
api.add_resource(UsersResource, '/users', '/users/<user_id>')
api.add_resource(ParkingSpots, '/spots', '/spots/<spot_id>')
api.add_resource(Reservations, '/reservations', '/reservations/<reservation_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(RegisterResource, '/register')


app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

cache.init_app(app)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(is_admin=True).first()

        if not admin:
            admin = User(username='admin', passhash='admin123', email='admin@admin.com', is_admin=True)
            users = [
                User(username='user1', passhash='user123', email='user1@user.com', is_admin=False),
                User(username='user2', passhash='user123', email='user2@user.com', is_admin=False),
                User(username='user3', passhash='user123', email='user3@user.com', is_admin=False),
                User(username='user4', passhash='user123', email='user4@user.com', is_admin=False)
            ]

            lots = [
                ParkingLot(location_name='Lot 1', price_per_hour=1000, address='123 Main St', pin_code='123456', number_of_spots=10),
                ParkingLot(location_name='Lot 2', price_per_hour=500, address='1234 Main St', pin_code='123457', number_of_spots=12),
                ParkingLot(location_name='Lot 3', price_per_hour=1500, address='1235 Main St', pin_code='123458', number_of_spots=14),
                ParkingLot(location_name='Lot 4', price_per_hour=750, address='1236 Main St', pin_code='123459', number_of_spots=20)
            ]

            db.session.add(admin)
            db.session.add_all(users)
            db.session.add_all(lots)
            db.session.commit()

            # Now generate spots for each lot
            for lot in lots:
                for i in range(1, lot.number_of_spots + 1):
                    spot = ParkingSpot(lot_id=lot.id, spot_number=i)
                    db.session.add(spot)

            db.session.commit()

        app.run(debug=True)
