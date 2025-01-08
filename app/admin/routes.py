from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models import User, Appointment
from app import db
from functools import wraps
from sqlalchemy import func, case
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            flash('You must be an admin to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_doctors = User.query.filter_by(user_type='doctor').count()
    total_patients = User.query.filter_by(user_type='patient').count()
    total_appointments = Appointment.query.count()
    
    # Get analytics data
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    # Weekly stats
    weekly_appointments = db.session.query(
        func.date(Appointment.created_at).label('date'),
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.created_at >= week_ago
    ).group_by(
        func.date(Appointment.created_at)
    ).all()
    
    weekly_users = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= week_ago
    ).group_by(
        func.date(User.created_at)
    ).all()
    
    # Appointment status distribution
    status_distribution = db.session.query(
        Appointment.status,
        func.count(Appointment.id).label('count')
    ).group_by(Appointment.status).all()
    
    # Get verified and unverified user counts
    verified_users = User.query.filter_by(is_verified=True).count()
    unverified_users = User.query.filter_by(is_verified=False).count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         recent_users=recent_users,
                         recent_appointments=recent_appointments,
                         weekly_appointments=weekly_appointments,
                         weekly_users=weekly_users,
                         status_distribution=status_distribution,
                         verified_users=verified_users,
                         unverified_users=unverified_users)

@admin.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    user_type = request.args.get('type', 'all')
    search = request.args.get('search', '')
    
    query = User.query
    if user_type != 'all':
        query = query.filter_by(user_type=user_type)
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/users.html', users=users, 
                         user_type=user_type, search=search)

@admin.route('/appointments')
@login_required
@admin_required
def appointments():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = Appointment.query
    if status != 'all':
        query = query.filter_by(status=status)
    if search:
        query = query.join(User, Appointment.patient_id == User.id)\
                    .filter(User.username.ilike(f'%{search}%'))
    
    appointments = query.order_by(Appointment.date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/appointments.html', 
                         appointments=appointments,
                         status=status, search=search)

@admin.route('/user/<int:user_id>/toggle-verification', methods=['POST'])
@login_required
@admin_required
def toggle_user_verification(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = not user.is_verified
    db.session.commit()
    flash(f'User {user.username} {"verified" if user.is_verified else "unverified"} successfully.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.user_type == 'admin':
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin.users'))
    
    # Delete all appointments where the user is either a patient or a doctor
    Appointment.query.filter((Appointment.patient_id == user.id) | 
                           (Appointment.doctor_id == user.id)).delete()
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} and their associated appointments deleted successfully.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/appointment/<int:appointment_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_appointment_status(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    status = request.form.get('status')
    if status in ['pending', 'confirmed', 'cancelled']:
        appointment.status = status
        db.session.commit()
        flash(f'Appointment status updated to {status}.', 'success')
    return redirect(url_for('admin.appointments'))

@admin.route('/analytics')
@login_required
@admin_required
def analytics():
    # Date range
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)
    
    # Daily appointments over time
    daily_appointments = db.session.query(
        func.date(Appointment.created_at).label('date'),
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.created_at >= start_date
    ).group_by(
        func.date(Appointment.created_at)
    ).all()
    
    # Doctor performance
    doctor_stats = db.session.query(
        User.username,
        func.count(Appointment.id).label('total_appointments'),
        func.sum(case(
            (Appointment.status == 'confirmed', 1),
            else_=0
        )).label('confirmed_appointments')
    ).join(
        Appointment, User.id == Appointment.doctor_id
    ).filter(
        User.user_type == 'doctor'
    ).group_by(User.id).all()
    
    # Specialization distribution
    specialization_stats = db.session.query(
        User.specialization,
        func.count(User.id).label('count')
    ).filter(
        User.user_type == 'doctor'
    ).group_by(User.specialization).all()
    
    return render_template('admin/analytics.html',
                         daily_appointments=daily_appointments,
                         doctor_stats=doctor_stats,
                         specialization_stats=specialization_stats)

@admin.route('/reports')
@login_required
@admin_required
def reports():
    report_type = request.args.get('type', 'appointments')
    start_date = request.args.get('start_date', (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.utcnow().strftime('%Y-%m-%d'))
    
    if report_type == 'appointments':
        data = Appointment.query.filter(
            Appointment.created_at.between(start_date, end_date)
        ).order_by(Appointment.created_at.desc()).all()
    elif report_type == 'users':
        data = User.query.filter(
            User.created_at.between(start_date, end_date)
        ).order_by(User.created_at.desc()).all()
    else:
        data = []
    
    return render_template('admin/reports.html',
                         report_type=report_type,
                         start_date=start_date,
                         end_date=end_date,
                         data=data)

@admin.route('/export-report')
@login_required
@admin_required
def export_report():
    report_type = request.args.get('type', 'appointments')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if report_type == 'appointments':
        data = Appointment.query.filter(
            Appointment.created_at.between(start_date, end_date)
        ).all()
        rows = [['ID', 'Patient', 'Doctor', 'Date', 'Status', 'Created At']]
        for item in data:
            rows.append([
                item.id,
                item.patient.username,
                item.doctor.username,
                item.date.strftime('%Y-%m-%d %H:%M'),
                item.status,
                item.created_at.strftime('%Y-%m-%d %H:%M')
            ])
    elif report_type == 'users':
        data = User.query.filter(
            User.created_at.between(start_date, end_date)
        ).all()
        rows = [['ID', 'Username', 'Email', 'Type', 'Verified', 'Created At']]
        for item in data:
            rows.append([
                item.id,
                item.username,
                item.email,
                item.user_type,
                'Yes' if item.is_verified else 'No',
                item.created_at.strftime('%Y-%m-%d %H:%M')
            ])
    
    return jsonify({
        'data': rows,
        'filename': f'{report_type}_report_{start_date}_to_{end_date}.csv'
    }) 