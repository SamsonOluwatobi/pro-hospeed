from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.email import send_email

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

@main.route('/test-email')
def test_email():
    try:
        send_email(
            subject='Test Email from HoSpeed',
            recipients=[current_app.config['ADMINS'][0]],
            html_body=render_template('email/test_email.html')
        )
        return 'Test email sent! Check your inbox.'
    except Exception as e:
        return f'Error sending email: {str(e)}' 