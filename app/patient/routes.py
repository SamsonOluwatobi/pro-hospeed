from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Schedule, Appointment, Referral
from datetime import datetime, timedelta
from app.patient.forms import AppointmentForm, SearchDoctorForm
from functools import wraps

patient = Blueprint('patient', __name__)

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'patient':
            flash('Access denied. Patient access only.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@patient.route('/dashboard')
@login_required
@patient_required
def dashboard():
    # Get upcoming appointments using proper SQLAlchemy query
    appointments = Appointment.query.filter_by(
        patient_id=current_user.id,
        status='confirmed'
    ).order_by(Appointment.date).all()
    
    # Get pending referrals using proper SQLAlchemy query
    referrals = Referral.query.filter_by(
        patient_id=current_user.id,
        status='pending'
    ).all()
    
    return render_template('patient/dashboard.html', 
                         appointments=appointments,
                         referrals=referrals)

@patient.route('/find-doctors', methods=['GET', 'POST'])
@login_required
@patient_required
def find_doctors():
    form = SearchDoctorForm()
    doctors = []
    
    if form.validate_on_submit() or request.args.get('specialization'):
        specialization = form.specialization.data or request.args.get('specialization')
        if specialization:
            doctors = User.query.filter_by(
                user_type='doctor',
                specialization=specialization
            ).all()
        else:
            # If no specialization selected, show all doctors
            doctors = User.query.filter_by(user_type='doctor').all()
    else:
        # By default, show all doctors
        doctors = User.query.filter_by(user_type='doctor').all()
    
    return render_template('patient/find_doctors.html', 
                         form=form, 
                         doctors=doctors)

@patient.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment(doctor_id):
    doctor = User.query.get_or_404(doctor_id)
    if doctor.user_type != 'doctor':
        flash('Invalid doctor selected.', 'danger')
        return redirect(url_for('patient.find_doctors'))

    form = AppointmentForm()
    # Get only available schedules for the select field
    available_schedules = Schedule.query.filter_by(
        doctor_id=doctor_id,
        is_available=True
    ).filter(
        Schedule.date >= datetime.now().date()
    ).order_by(Schedule.date, Schedule.start_time).all()
    
    form.schedule_id.choices = [
        (s.id, f"{s.date.strftime('%B %d, %Y')} at {s.start_time.strftime('%I:%M %p')}")
        for s in available_schedules
    ]

    if form.validate_on_submit():
        schedule = Schedule.query.get(form.schedule_id.data)
        if not schedule or not schedule.is_available:
            flash('Selected time slot is no longer available.', 'danger')
            return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))

        try:
            appointment = Appointment(
                doctor_id=doctor_id,
                patient_id=current_user.id,
                schedule_id=schedule.id,
                date=datetime.combine(schedule.date, schedule.start_time),
                symptoms=form.symptoms.data,
                notes=form.notes.data
            )
            schedule.is_available = False
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient.appointments'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the appointment.', 'danger')

    return render_template('patient/book_appointment.html', form=form, doctor=doctor)

@patient.route('/appointments')
@login_required
@patient_required
def appointments():
    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(Appointment.date.desc()).all()
    
    return render_template('patient/appointments.html', appointments=appointments)

@patient.route('/referrals')
@login_required
@patient_required
def referrals():
    referrals = Referral.query.filter_by(
        patient_id=current_user.id
    ).order_by(Referral.created_at.desc()).all()
    
    return render_template('patient/referrals.html', referrals=referrals)

@patient.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(appointment_id):
    """Cancel an appointment."""
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment not in current_user.appointments_as_patient:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        appointment.status = 'cancelled'
        # Make the schedule available again
        appointment.schedule.is_available = True
        db.session.commit()
        return jsonify({'message': 'Appointment cancelled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 