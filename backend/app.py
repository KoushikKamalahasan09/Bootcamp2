from flask import Flask, render_template, request
from flask_cors import CORS
from models import db,User
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash

app = Flask(__name__)
api = Api(app)

CORS(app)

# connecting database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'c5faf247641cfc78c25d4b2ccd1bb07d079cbe3a31310aed98cbb4c62b4cc003'

db.init_app(app)

# connecting api resources to endpoints
from controllers import Parkinglots,UsersResource,ParkingSpots,Reservations

api.add_resource(Parkinglots, '/lots', '/lots/<lot_id>')
api.add_resource(UsersResource, '/users', '/users/<user_id>')
api.add_resource(ParkingSpots, '/spots', '/spots/<spot_id>')
api.add_resource(Reservations, '/reservations', '/reservations/<reservation_id>')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(" Tables created")
        
        admin=User.query.filter_by(is_admin=True).first()
        
        if not admin:
            admin = User(username='admin',passhash=generate_password_hash('admin123'),email='admin@admin.com', is_admin=True)
            db.session.add(admin)
            db.session.commit()
        
        app.run(debug=True)