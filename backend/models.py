from datetime import datetime
from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='trekker')  
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade="all, delete")
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete")

    
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True)


class Trek(db.Model):
    __tablename__ = 'treks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  
    duration_days = db.Column(db.Integer, nullable=False)

    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    status = db.Column(db.String(20), default='pending', nullable=False)  

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    price = db.Column(db.Float, default=0.0)

    
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade="all, delete")
    reviews = db.relationship('Review', backref='trek', lazy=True, cascade="all, delete")


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default='booked', nullable=False)  
    payment_status = db.Column(db.String(20), default='pending')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)