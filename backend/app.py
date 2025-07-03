from flask import Flask, render_template, request
from flask_cors import CORS
from models import db,User
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from controllers import Parkinglots,UsersResource,ParkingSpots,Reservations,LoginResource
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
            
            db.session.add(admin)
            db.session.add(User1)
            db.session.add(User2)
            db.session.add(User3)
            db.session.add(User4)
            db.session.commit()
        
        app.run(debug=True)