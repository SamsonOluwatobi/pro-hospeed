from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from app.models import User

class SearchDoctorForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[
        ('', 'Select Specialization'),
        ('general', 'General Physician'),
        ('pediatrician', 'Pediatrician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('orthopedic', 'Orthopedic Surgeon'),
        ('gynecologist', 'Gynecologist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('dentist', 'Dentist')
    ])
    submit = SubmitField('Search')

class AppointmentForm(FlaskForm):
    schedule_id = SelectField('Available Time Slots', coerce=int, validators=[DataRequired()])
    symptoms = TextAreaField('Symptoms', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes')
    submit = SubmitField('Book Appointment') 