from flask import Flask, render_template, request
from flask_cors import CORS
from models import db,User,ParkingLot,ParkingSpot,Reservation
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from controllers import Parkinglots,UsersResource,ParkingSpots,Reservations,LoginResource,RegisterResource,ReportGenerate
from controllers import cache
from datetime import datetime,timedelta

now =datetime.now()

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
api.add_resource(UsersResource, '/users', '/users/<user_id>','/users/count')
api.add_resource(ParkingSpots, '/spots', '/spots/<spot_id>')
api.add_resource(Reservations, '/reservations', '/reservations/<reservation_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(RegisterResource, '/register')
api.add_resource(ReportGenerate, '/generate_report', '/generate_report/<int:user_id>')


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
                ParkingLot(location_name='Lot 1', price_per_hour=1000, address='123 Main St', pin_code='123456', number_of_spots=4),
                ParkingLot(location_name='Lot 2', price_per_hour=500, address='1234 Main St', pin_code='123457', number_of_spots=5),
                ParkingLot(location_name='Lot 3', price_per_hour=1500, address='1235 Main St', pin_code='123458', number_of_spots=6),
                ParkingLot(location_name='Lot 4', price_per_hour=750, address='1236 Main St', pin_code='123459', number_of_spots=7)
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
            
            Res = [
                    Reservation(user_id=2, spot_id=3,
                                parking_timestamp=now + timedelta(hours=1),
                                leaving_timestamp=now + timedelta(hours=3)),

                    Reservation(user_id=3, spot_id=18,
                                parking_timestamp=now + timedelta(hours=2),
                                leaving_timestamp=now + timedelta(hours=4)),

                    Reservation(user_id=4, spot_id=20,
                                parking_timestamp=now + timedelta(hours=3),
                                leaving_timestamp=now + timedelta(hours=5)),

                    Reservation(user_id=2, spot_id=15,
                                parking_timestamp=now + timedelta(hours=4),
                                leaving_timestamp=now + timedelta(hours=6)),

                    Reservation(user_id=3, spot_id=13,
                                parking_timestamp=now + timedelta(hours=5),
                                leaving_timestamp=now + timedelta(hours=7)),

                    Reservation(user_id=4, spot_id=22,
                                parking_timestamp=now + timedelta(hours=6),
                                leaving_timestamp=now + timedelta(hours=8)),

                    Reservation(user_id=2, spot_id=8,
                                parking_timestamp=now + timedelta(hours=7),
                                leaving_timestamp=now + timedelta(hours=9)),
                    Reservation(user_id=2, spot_id=7,
                                parking_timestamp=now - timedelta(days=33,hours=8),
                                leaving_timestamp=now - timedelta(days=26,hours=10)),
                    Reservation(user_id=3, spot_id=14,
                                parking_timestamp=now - timedelta(days=30,hours=8),
                                leaving_timestamp=now - timedelta(days=20,hours=10)),
                    Reservation(user_id=4, spot_id=2,
                                parking_timestamp=now - timedelta(days=43,hours=8),
                                leaving_timestamp=now - timedelta(days=30,hours=10)),
                    Reservation(user_id=5, spot_id=19,
                                parking_timestamp=now - timedelta(days=61,hours=8),
                                leaving_timestamp=now - timedelta(days=37,hours=10))]
            db.session.add_all(Res)
            db.session.commit()    
            
        
        app.run(debug=True)
