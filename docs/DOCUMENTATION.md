# HoSpeed Technical Documentation

## System Architecture

### Overview
HoSpeed follows a Model-View-Controller (MVC) architecture pattern using Flask blueprints for modular organization. The application is structured to handle healthcare appointment management with separate modules for different user roles.

### Components

#### 1. Authentication System
- Uses Flask-Login for session management
- JWT-based email verification and password reset
- Bcrypt password hashing
- Role-based access control (Patient, Doctor, Admin)

#### 2. Database Schema
```sql
User
- id (PK)
- username
- email
- password_hash
- user_type
- is_verified
- created_at
- specialization (for doctors)
- license_number (for doctors)
- clinic_address (for doctors)
- latitude
- longitude

Appointment
- id (PK)
- patient_id (FK)
- doctor_id (FK)
- date
- status
- notes
- created_at
```

#### 3. Email System
- Flask-Mail integration
- Asynchronous email sending
- HTML email templates with responsive design
- Email verification and notifications
- Appointment reminders

#### 4. Security Measures
- CSRF protection on all forms
- SQL injection prevention through SQLAlchemy
- XSS protection in templates
- Secure session configuration
- Rate limiting on sensitive endpoints
- Input validation and sanitization

## API Reference

### Authentication API

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secretpassword
```

Response:
```json
{
    "status": "success",
    "message": "Login successful",
    "redirect": "/dashboard"
}
```

#### Registration
```http
POST /auth/signup
Content-Type: application/x-www-form-urlencoded

username=newuser&email=user@example.com&password=secretpassword&user_type=patient
```

### Appointment API

#### Book Appointment
```http
POST /patient/book-appointment
Content-Type: application/x-www-form-urlencoded

doctor_id=1&date=2024-01-30T14:00:00&notes=Regular checkup
```

#### Update Appointment Status
```http
POST /doctor/appointment/<id>/status
Content-Type: application/x-www-form-urlencoded

status=confirmed
```

## Frontend Components

### Templates
- Base template with common layout
- User role-specific dashboards
- Responsive design using Bootstrap 5
- Custom CSS with modern styling
- Interactive components with JavaScript

### JavaScript Modules
- Appointment booking validation
- Real-time form validation
- Dynamic content loading
- Interactive maps for doctor locations
- Alert system

## Development Guide

### Setting Up Development Environment

1. Database Setup
```bash
# Create database
createdb hospeed_dev

# Run migrations
flask db upgrade
```

2. Email Configuration
```python
# config.py
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-specific-password'
```

3. Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
coverage run -m pytest
```

### Code Style Guide

#### Python
- Follow PEP 8 guidelines
- Use type hints where applicable
- Document functions and classes
- Keep functions focused and small

Example:
```python
def send_appointment_reminder(appointment_id: int) -> bool:
    """
    Send reminder email for upcoming appointment.
    
    Args:
        appointment_id: The ID of the appointment
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        send_email(
            subject="Appointment Reminder",
            recipients=[appointment.patient.email],
            html_body=render_template(
                'email/appointment_reminder.html',
                appointment=appointment
            )
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send reminder: {str(e)}")
        return False
```

#### HTML/CSS
- Use semantic HTML5 elements
- Follow BEM naming convention
- Maintain responsive design
- Keep CSS modular

### Deployment Process

1. Pre-deployment Checklist
- Run all tests
- Check dependencies
- Update documentation
- Review security settings

2. Deployment Steps
```bash
# 1. Update requirements
pip freeze > requirements.txt

# 2. Run tests
pytest

# 3. Create production database backup
pg_dump hospeed_db > backup.sql

# 4. Deploy to Render
git push origin main
```

3. Post-deployment Verification
- Check all endpoints
- Verify email functionality
- Test user workflows
- Monitor error logs

## Maintenance

### Backup Procedures
- Daily database backups
- Weekly full system backups
- Store backups in secure location

### Monitoring
- Use Render dashboard
- Monitor error logs
- Track system metrics
- Check email delivery status

### Updates and Patches
- Regular dependency updates
- Security patch application
- Database optimization
- Performance monitoring

## Troubleshooting

### Common Issues

1. Email Delivery
- Check SMTP settings
- Verify sender email
- Check spam settings
- Review email templates

2. Database
- Connection issues
- Migration errors
- Query performance
- Backup/restore

3. Authentication
- Session issues
- Password reset
- Email verification
- Role permissions

### Error Codes

```python
ERROR_CODES = {
    'AUTH001': 'Invalid credentials',
    'AUTH002': 'Email not verified',
    'APP001': 'Invalid appointment time',
    'APP002': 'Doctor unavailable',
    'SYS001': 'Database connection error',
    'SYS002': 'Email service error'
}
```

## Support

### Contact Information
- Technical Support: samtob2002@gmail.com
- Bug Reports: GitHub Issues
- Feature Requests: GitHub Discussions

### Resources
- GitHub Repository
- API Documentation
- User Guide
- Contributing Guide 