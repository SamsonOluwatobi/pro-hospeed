# HoSpeed - Healthcare at the Speed of Life 🏥

HoSpeed is a modern healthcare appointment management system that connects patients with healthcare providers efficiently and securely.

## Features ✨

- **User Management**
  - Patient and Doctor registration
  - Email verification
  - Secure authentication
  - Profile management

- **Appointment System**
  - Easy appointment scheduling
  - Real-time availability checking
  - Appointment confirmation emails
  - Automated reminders
  - Rescheduling and cancellation

- **Doctor Features**
  - Customizable schedule management
  - Patient history access
  - Appointment notifications
  - Clinic location management

- **Patient Features**
  - Doctor search and filtering
  - Appointment history
  - Medical record uploads
  - Email notifications

- **Admin Dashboard**
  - User management
  - Analytics and reporting
  - System monitoring
  - Content management

## Technology Stack 🛠️

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Authentication**: Flask-Login
- **Email**: Flask-Mail
- **Frontend**: Bootstrap 5, JavaScript
- **Deployment**: Render
- **Version Control**: Git

## Prerequisites 📋

- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- Virtual environment (recommended)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/SamsonOluwatobi/pro-hospeed.git
cd pro-hospeed
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `SECRET_KEY`: Application secret key
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `MAIL_SERVER`: SMTP server address
- `MAIL_PORT`: SMTP server port
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password
- `MAIL_USE_TLS`: Use TLS (True/False)
- `MAIL_USE_SSL`: Use SSL (True/False)
- `ADMIN_EMAIL`: Admin email address

5. Initialize the database:
```bash
flask db upgrade
```

6. Create admin user:
```bash
flask create-admin
```

7. Run the development server:
```bash
flask run
```

## Project Structure 📁

```
hospeed/
├── app/
│   ├── admin/         # Admin routes and functionality
│   ├── auth/          # Authentication routes and forms
│   ├── doctor/        # Doctor-specific functionality
│   ├── patient/       # Patient-specific functionality
│   ├── static/        # Static files (CSS, JS, images)
│   ├── templates/     # HTML templates
│   ├── email.py       # Email functionality
│   ├── models.py      # Database models
│   └── __init__.py    # App initialization
├── migrations/        # Database migrations
├── tests/            # Test files
├── config.py         # Configuration settings
├── requirements.txt  # Project dependencies
└── wsgi.py          # WSGI entry point
```

## API Documentation 📚

### Authentication Endpoints

- `POST /auth/login`: User login
- `POST /auth/signup`: User registration
- `GET /auth/verify-email/<token>`: Email verification
- `POST /auth/reset-password`: Password reset request
- `POST /auth/reset-password/<token>`: Password reset confirmation

### Patient Endpoints

- `GET /patient/dashboard`: Patient dashboard
- `GET /patient/appointments`: List patient appointments
- `POST /patient/book-appointment`: Book new appointment
- `POST /patient/cancel-appointment/<id>`: Cancel appointment

### Doctor Endpoints

- `GET /doctor/dashboard`: Doctor dashboard
- `GET /doctor/appointments`: List doctor appointments
- `POST /doctor/update-schedule`: Update availability
- `POST /doctor/appointment/<id>/status`: Update appointment status

## Security Features 🔒

- Password hashing using bcrypt
- CSRF protection
- Email verification
- Secure session management
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## Contributing 🤝

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## Testing 🧪

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
coverage run -m pytest
coverage report
```

## Deployment 🌐

The application is deployed on Render. For deployment:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables
4. Deploy the main branch

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support, please contact:
- Email: samtob2002@gmail.com
- GitHub Issues: [Create an issue](https://github.com/SamsonOluwatobi/pro-hospeed/issues)

## Contributors 👥

- Samson Lana - Backend Developer
- Kevin Amoni - Backend Developer

## Acknowledgments 🙏

- Flask documentation and community
- Bootstrap team
- All contributors and users 