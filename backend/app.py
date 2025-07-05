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
        #print(" Tables created")
        
        admin=User.query.filter_by(is_admin=True).first()
        
        if not admin:
            admin = User(username='admin',passhash='admin123',email='admin@admin.com', is_admin=True)
            User1=User(username='user1',passhash='user123',email='user1@user.com', is_admin=False)
            User2=User(username='user2',passhash='user123',email='user2@user.com', is_admin=False)
            User3=User(username='user3',passhash='user123',email='user3@user.com', is_admin=False)
            User4=User(username='user4',passhash='user123',email='user4@user.com', is_admin=False)
            Lot1=ParkingLot(location_name='Lot 1', price_per_hour=1000, address='123 Main St', pin_code='123456', number_of_spots=50)
            Lot2=ParkingLot(location_name='Lot 2', price_per_hour=500, address='1234 Main St', pin_code='123457', number_of_spots=150)
            Lot3=ParkingLot(location_name='Lot 3', price_per_hour=1500, address='1235 Main St', pin_code='123458', number_of_spots=250)
            Lot4=ParkingLot(location_name='Lot 4', price_per_hour=750, address='1236 Main St', pin_code='123459', number_of_spots=350)
            Spot1_1=ParkingSpot(lot_id=1, spot_number=1, is_avail=True)
            Spot1_2=ParkingSpot(lot_id=1, spot_number=2, is_avail=True)
            Spot2_1=ParkingSpot(lot_id=2, spot_number=1, is_avail=True)
            Spot2_2=ParkingSpot(lot_id=2, spot_number=2, is_avail=True)
            Spot3_1=ParkingSpot(lot_id=3, spot_number=1, is_avail=True)
            Spot3_2=ParkingSpot(lot_id=3, spot_number=2, is_avail=True)
            Spot4_1=ParkingSpot(lot_id=4, spot_number=1, is_avail=True)
            Spot4_2=ParkingSpot(lot_id=4, spot_number=2, is_avail=True)
            

            db.session.add(admin)
            db.session.add(User1)
            db.session.add(User2)
            db.session.add(User3)
            db.session.add(User4)
            db.session.add(Lot1)
            db.session.add(Lot2)
            db.session.add(Lot3)
            db.session.add(Lot4)
            db.session.add(Spot1_1)
            db.session.add(Spot1_2)
            db.session.add(Spot2_1)
            db.session.add(Spot2_2)
            db.session.add(Spot3_1)
            db.session.add(Spot3_2)
            db.session.add(Spot4_1)
            db.session.add(Spot4_2)
            db.session.commit()
        
        app.run(debug=True)