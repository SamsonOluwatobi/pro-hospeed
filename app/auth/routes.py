from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.auth.forms import LoginForm, SignupForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from app.email import send_verification_email, send_password_reset_email
from urllib.parse import urlparse
import traceback

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        if current_user.user_type == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.user_type == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        else:
            return redirect(url_for('patient.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            if user.user_type == 'admin':
                next_page = url_for('admin.dashboard')
            elif user.user_type == 'doctor':
                next_page = url_for('doctor.dashboard')
            else:
                next_page = url_for('patient.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data.lower(),
                user_type=form.user_type.data
            )
            
            # Set doctor-specific fields if user is a doctor
            if form.user_type.data == 'doctor':
                user.specialization = form.specialization.data
                user.license_number = form.license_number.data
                user.clinic_address = form.clinic_address.data
                user.latitude = float(form.latitude.data)
                user.longitude = float(form.longitude.data)
            
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            # Send verification email
            try:
                send_verification_email(user)
                flash('Congratulations, you are now registered! Please check your email to verify your account.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                print(f"Error sending verification email: {str(e)}")
                print(traceback.format_exc())
                flash('Registration successful but there was an error sending the verification email. Please contact support.', 'warning')
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            print(traceback.format_exc())
            db.session.rollback()
            flash('An error occurred during registration.', 'danger')
            return redirect(url_for('auth.signup'))
    
    return render_template('auth/signup.html', title='Sign Up', form=form)

@auth.route('/verify-email/<token>')
def verify_email(token):
    """Verify user's email with token."""
    if current_user.is_authenticated and current_user.is_verified:
        return redirect(url_for('main.index'))
    
    user = User.verify_email_token(token)
    if not user:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('main.index'))
    
    user.is_verified = True
    db.session.commit()
    flash('Your email has been verified! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/resend-verification')
@login_required
def resend_verification():
    """Resend verification email."""
    if current_user.is_verified:
        return redirect(url_for('main.index'))
    
    try:
        send_verification_email(current_user)
        flash('A new verification email has been sent. Please check your inbox.', 'info')
    except Exception as e:
        print(f"Error resending verification email: {str(e)}")
        print(traceback.format_exc())
        flash('Error sending verification email. Please try again later.', 'danger')
    
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handle password change."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Current password is incorrect.', 'danger')
    return render_template('auth/change_password.html', form=form)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user)
        flash('If an account exists with that email, we have sent a password reset link.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', title='Reset Password', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form) 