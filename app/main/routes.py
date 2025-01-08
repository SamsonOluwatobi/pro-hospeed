from flask import Blueprint, render_template, current_app, flash, redirect, url_for
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
        # Get admin email from config
        admin_email = current_app.config['ADMINS'][0]
        
        # Send test email
        send_email(
            subject='Test Email from HoSpeed',
            recipients=[admin_email],
            html_body=render_template('email/test_email.html')
        )
        flash('Test email sent successfully! Please check your inbox.', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.error(f'Error sending test email: {str(e)}')
        flash(f'Error sending email: {str(e)}', 'error')
        return redirect(url_for('main.index')) 