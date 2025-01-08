from flask import current_app, render_template
from flask_mail import Message, Mail
from threading import Thread
from datetime import datetime

mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {str(e)}")

def send_email(subject, recipients, html_body):
    msg = Message(
        subject=subject,
        sender=('HoSpeed Healthcare', current_app.config['MAIL_USERNAME']),
        recipients=recipients,
        html=html_body
    )
    
    # Add headers to improve deliverability
    msg.extra_headers = {
        'List-Unsubscribe': '<mailto:' + current_app.config['MAIL_USERNAME'] + '?subject=unsubscribe>',
        'Precedence': 'bulk',
        'Auto-Submitted': 'auto-generated',
        'X-Mailer': 'HoSpeed Healthcare Platform'
    }
    
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[HoSpeed] Reset Your Password',
        recipients=[user.email],
        html_body=render_template('email/reset_password.html',
                                user=user, token=token,
                                current_year=datetime.now().year)
    )

def send_verification_email(user):
    token = user.get_verification_token()
    send_email(
        '[HoSpeed] Verify Your Email',
        recipients=[user.email],
        html_body=render_template('email/verify_email.html',
                                user=user, token=token,
                                current_year=datetime.now().year)
    )

def send_appointment_confirmation(appointment):
    send_email(
        '[HoSpeed] Appointment Confirmation',
        recipients=[appointment.patient.email],
        html_body=render_template('email/appointment_confirmation.html',
                                appointment=appointment,
                                current_year=datetime.now().year)
    )

def send_appointment_reminder(appointment):
    send_email(
        '[HoSpeed] Appointment Reminder',
        recipients=[appointment.patient.email],
        html_body=render_template('email/appointment_reminder.html',
                                appointment=appointment,
                                current_year=datetime.now().year)
    )

def send_doctor_notification(appointment):
    send_email(
        '[HoSpeed] New Appointment Request',
        recipients=[appointment.doctor.email],
        html_body=render_template('email/doctor_notification.html',
                                appointment=appointment,
                                current_year=datetime.now().year)
    ) 