from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# User model
class User(db.Model):
    
    __tablename__ = 'users'
    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }


# Parking lot model
class ParkingLot(db.Model):
    
    __tablename__ = 'parking_lots'
    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete-orphan", lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'price_per_hour': self.price_per_hour,
            'address': self.address,
            'pin_code': self.pin_code,
            'number_of_spots': self.number_of_spots
        }
        

# Parking spot model
class ParkingSpot(db.Model):
    
    __tablename__ = 'parking_spots'
    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    is_avail = db.Column(db.Boolean, default=True, nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'is_avail': self.is_avail,
            'spot_number': self.spot_number
        }


# Reservation model
class Reservation(db.Model):
    
    __tablename__ = 'reservations'



    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at= db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'spot_id': self.spot_id,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'parking_cost': self.parking_cost,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
