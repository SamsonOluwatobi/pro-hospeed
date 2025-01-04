from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from . import db
from .models import User, Appointment
from flask_login import current_user

api = Blueprint('api', __name__)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Hash this in production!
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@api.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    appointment = Appointment(
        doctor_id=data['doctor_id'],
        patient_id=data['patient_id'],
        date=data['date']
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment booked successfully"}), 201

@api.route('/appointments/<int:doctor_id>', methods=['GET'])
def get_appointments(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([{
        "id": a.id,
        "patient_id": a.patient_id,
        "date": a.date,
        "status": a.status
    } for a in appointments]), 200

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_type == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        else:
            return redirect(url_for('patient.dashboard'))
    return render_template('main/index.html')
