from flask import current_app, render_template
from flask_mail import Message
import requests
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            mailgun_domain = app.config['MAILGUN_DOMAIN']
            mailgun_api_key = app.config['MAILGUN_API_KEY']
            
            response = requests.post(
                f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"HoSpeed <mailgun@{mailgun_domain}>",
                    "to": msg.recipients,
                    "subject": msg.subject,
                    "html": msg.html
                }
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending email: {str(e)}")

def send_email(subject, recipients, html_body):
    msg = Message(subject=subject, recipients=recipients, html=html_body)
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[HoSpeed] Reset Your Password',
        recipients=[user.email],
        html_body=render_template('email/reset_password.html',
                                user=user, token=token)
    )

def send_verification_email(user):
    token = user.get_verification_token()
    send_email(
        '[HoSpeed] Verify Your Email',
        recipients=[user.email],
        html_body=render_template('email/verify_email.html',
                                user=user, token=token)
    )

def send_appointment_confirmation(appointment):
    send_email(
        '[HoSpeed] Appointment Confirmation',
        recipients=[appointment.patient.email],
        html_body=render_template('email/appointment_confirmation.html',
                                appointment=appointment)
    )

def send_appointment_reminder(appointment):
    send_email(
        '[HoSpeed] Appointment Reminder',
        recipients=[appointment.patient.email],
        html_body=render_template('email/appointment_reminder.html',
                                appointment=appointment)
    )

def send_doctor_notification(appointment):
    send_email(
        '[HoSpeed] New Appointment Request',
        recipients=[appointment.doctor.email],
        html_body=render_template('email/doctor_notification.html',
                                appointment=appointment)
    ) 