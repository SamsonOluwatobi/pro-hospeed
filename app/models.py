from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from time import time
import jwt
from flask import current_app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False)  # 'patient' or 'doctor'
    is_verified = db.Column(db.Boolean, default=False)
    
    # Doctor-specific fields
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    clinic_address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Appointment relationships with explicit foreign keys
    appointments_as_doctor = db.relationship(
        'Appointment',
        foreign_keys='Appointment.doctor_id',
        backref='doctor',
        lazy=True
    )
    
    appointments_as_patient = db.relationship(
        'Appointment',
        foreign_keys='Appointment.patient_id',
        backref='patient',
        lazy=True
    )
    
    # Schedule relationship
    schedules = db.relationship('Schedule', backref='doctor', lazy=True)
    
    # Referral relationships
    referrals_given = db.relationship(
        'Referral',
        foreign_keys='Referral.referring_doctor_id',
        backref='referring_doctor',
        lazy=True
    )
    
    referrals_received = db.relationship(
        'Referral',
        foreign_keys='Referral.referred_doctor_id',
        backref='referred_doctor',
        lazy=True
    )
    
    referrals_as_patient = db.relationship(
        'Referral',
        foreign_keys='Referral.patient_id',
        backref='patient',
        lazy=True
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=3600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    def get_verification_token(self, expires_in=86400):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
            return User.query.get(id)
        except:
            return None
    
    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['verify_email']
            return User.query.get(id)
        except:
            return None
    
    def __repr__(self):
        return f'<User {self.username}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    schedule = db.relationship('Schedule', backref='appointments')
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referring_doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
