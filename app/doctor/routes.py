from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Schedule, Appointment, Referral
from datetime import datetime, timedelta
from app.doctor.forms import ScheduleForm, ReferralForm
from functools import wraps
from functools import wraps

doctor = Blueprint('doctor', __name__)
def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'doctor':
            flash('Access denied. Doctor privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'doctor':
            flash('Access denied. Doctor privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@doctor.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    # Get today's appointments using proper SQLAlchemy query
    today = datetime.now().date()
    appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.date >= today,
        Appointment.date < today + timedelta(days=1)
    ).order_by(Appointment.date).all()
    
    # Get pending referrals count
    pending_referrals = len([r for r in current_user.referrals_received if r.status == 'pending'])
    
    return render_template('doctor/dashboard.html', 
                         appointments=appointments,
                         pending_referrals=pending_referrals)

@doctor.route('/schedule', methods=['GET', 'POST'])
@login_required
def manage_schedule():
    if current_user.user_type != 'doctor':
        flash('Access denied. Doctor privileges required.', 'danger')
        return redirect(url_for('main.index'))

    form = ScheduleForm()
    if form.validate_on_submit():
        try:
            schedule = Schedule(
                doctor_id=current_user.id,
                date=form.date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Schedule added successfully!', 'success')
            return redirect(url_for('doctor.manage_schedule'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the schedule.', 'danger')
            return redirect(url_for('doctor.manage_schedule'))

    schedules = Schedule.query.filter_by(doctor_id=current_user.id).order_by(Schedule.date, Schedule.start_time).all()
    return render_template('doctor/schedule.html', form=form, schedules=schedules)

@doctor.route('/appointments')
@login_required
def appointments():
    if current_user.user_type != 'doctor':
        flash('Access denied. Doctor privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    appointments = Appointment.query.filter_by(doctor_id=current_user.id).order_by(Appointment.date.desc()).all()
    return render_template('doctor/appointments.html', appointments=appointments)

@doctor.route('/referral/new', methods=['GET', 'POST'])
@login_required
def create_referral():
    if current_user.user_type != 'doctor':
        flash('Access denied. Doctor privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get list of patients who have had appointments with this doctor
    patients_with_appointments = User.query.join(Appointment, User.id == Appointment.patient_id)\
        .filter(Appointment.doctor_id == current_user.id)\
        .distinct().all()
    
    if not patients_with_appointments:
        flash('You have no patients to refer. You can only refer patients who have had appointments with you.', 'info')
        return redirect(url_for('doctor.dashboard'))
    
    form = ReferralForm()
    # Update patient choices to only include patients with appointments
    form.patient_id.choices = [(p.id, p.username) for p in patients_with_appointments]
    
    if form.validate_on_submit():
        try:
            referral = Referral(
                patient_id=form.patient_id.data,
                referring_doctor_id=current_user.id,
                referred_doctor_id=form.referred_doctor_id.data,
                reason=form.reason.data,
                notes=form.notes.data
            )
            db.session.add(referral)
            db.session.commit()
            flash('Referral created successfully!', 'success')
            return redirect(url_for('doctor.manage_referrals'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the referral.', 'danger')
            return redirect(url_for('doctor.create_referral'))
    
    return render_template('doctor/create_referral.html', form=form)

@doctor.route('/appointments/<int:appointment_id>/status', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    """Update the status of an appointment."""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    # Use the new relationship to verify ownership
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment not in current_user.appointments_as_doctor:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['confirmed', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400

    try:
        appointment.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@doctor.route('/referrals')
@login_required
def manage_referrals():
    if current_user.user_type != 'doctor':
        flash('Access denied. Doctor privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    sent_referrals = Referral.query.filter_by(
        referring_doctor_id=current_user.id
    ).order_by(Referral.created_at.desc()).all()
    
    received_referrals = Referral.query.filter_by(
        referred_doctor_id=current_user.id
    ).order_by(Referral.created_at.desc()).all()
    
    return render_template('doctor/referrals.html',
                         sent_referrals=sent_referrals,
                         received_referrals=received_referrals)

@doctor.route('/referrals/<int:referral_id>/status', methods=['POST'])
@login_required
def update_referral_status(referral_id):
    """Update the status of a referral."""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    referral = Referral.query.get_or_404(referral_id)
    
    # Verify the referral belongs to this doctor
    if referral not in current_user.referrals_received:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['accepted', 'completed', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    try:
        referral.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@doctor.route('/schedule/<int:schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    """Delete a schedule slot."""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403

    schedule = Schedule.query.get_or_404(schedule_id)
    
    # Verify the schedule belongs to this doctor
    if schedule.doctor_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Check if the schedule has any appointments
    if not schedule.is_available:
        return jsonify({'error': 'Cannot delete booked schedule'}), 400

    try:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'message': 'Schedule deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@doctor.route('/api/appointments/today')
@login_required
def get_today_appointments():
    """API endpoint to get today's appointments."""
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    today = datetime.now().date()
    appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.date >= today,
        Appointment.date < today + timedelta(days=1)
    ).order_by(Appointment.date).all()
    
    return jsonify([{
        'id': apt.id,
        'patient_name': apt.patient.username,
        'time': apt.date.strftime('%I:%M %p'),
        'status': apt.status,
        'symptoms': apt.symptoms
    } for apt in appointments]) 