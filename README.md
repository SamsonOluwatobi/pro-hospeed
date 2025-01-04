# HoSpeed - Healthcare Appointment Management System

HoSpeed is a modern web application that streamlines the healthcare appointment booking process, connecting patients with healthcare providers efficiently.

## Features

- **Smart Doctor Search**: Find healthcare providers based on specialization and location
- **Real-time Appointment Booking**: Book and manage appointments with instant confirmation
- **Integrated Referral System**: Seamless referrals between healthcare providers
- **User-friendly Dashboard**: Separate interfaces for doctors and patients
- **Schedule Management**: Doctors can manage their availability and appointments
- **Location-based Services**: Find nearby healthcare providers using maps

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Maps**: Leaflet.js
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hospeed
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the development server:
```bash
flask run
```

## Project Structure

```
hospeed/
├── app/
│   ├── auth/          # Authentication routes and forms
│   ├── doctor/        # Doctor-specific functionality
│   ├── patient/       # Patient-specific functionality
│   ├── main/          # Main routes
│   ├── templates/     # HTML templates
│   ├── models.py      # Database models
│   └── __init__.py    # App initialization
├── migrations/        # Database migrations
├── requirements.txt   # Project dependencies
└── config.py         # Configuration settings
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact [Your Contact Information]. 