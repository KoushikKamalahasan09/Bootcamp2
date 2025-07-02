from flask import Flask, render_template, request
from flask_cors import CORS

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

CORS(app)

# connecting database
from models import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
db.init_app(app)

# connecting api resources to endpoints
from controllers import Parkinglots

api.add_resource(Parkinglots, '/lots', '/lots/<lot_id>')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)