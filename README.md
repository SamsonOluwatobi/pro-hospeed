# HoSpeed - Healthcare Appointment Management System

A modern healthcare appointment management system built with Flask, featuring patient-doctor scheduling, real-time location tracking, and email notifications.

## Features

- User Authentication (Patient, Doctor, Admin)
- Appointment Scheduling
- Real-time Doctor Location Tracking
- Email Notifications
- Admin Dashboard
- Responsive Design

## Tech Stack

- Backend: Flask (Python)
- Database: SQLAlchemy
- Frontend: Bootstrap 5, JavaScript
- Maps: Leaflet.js
- Email: Mailgun
- Deployment: Vercel

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pro-hospeed
```

2. Create a virtual environment:
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

6. Create an admin user:
```bash
flask create-admin
```

7. Run the development server:
```bash
flask run
```

## Deployment on Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. Set up environment variables on Vercel:
- Go to your project settings
- Add the required environment variables from your .env file

## Version Control

This project uses Git for version control. Here are some common commands:

```bash
# Create a new branch
git checkout -b feature/new-feature

# Stage changes
git add .

# Commit changes
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature

# Merge changes
git checkout main
git merge feature/new-feature
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 