from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, Length
from app.models import User

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Sign up as', choices=[
        ('patient', 'Patient'),
        ('doctor', 'Doctor')
    ], validators=[DataRequired()])
    
    # Doctor-specific fields
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
    ], validators=[Optional()])
    license_number = StringField('Medical License Number', validators=[Optional()])
    clinic_address = TextAreaField('Clinic Address', validators=[Optional()])
    location_method = SelectField('Choose Location Input Method', choices=[
        ('manual', 'Enter Coordinates Manually'),
        ('map', 'Pick from Map'),
        ('current', 'Use Current Location')
    ], validators=[Optional()])
    latitude = StringField('Latitude', validators=[Optional()])
    longitude = StringField('Longitude', validators=[Optional()])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
    
    def validate_specialization(self, field):
        if self.user_type.data == 'doctor' and not field.data:
            raise ValidationError('Specialization is required for doctors.')
    
    def validate_license_number(self, field):
        if self.user_type.data == 'doctor' and not field.data:
            raise ValidationError('License number is required for doctors.')
    
    def validate_clinic_address(self, field):
        if self.user_type.data == 'doctor' and not field.data:
            raise ValidationError('Clinic address is required for doctors.')
    
    def validate_latitude(self, field):
        if self.user_type.data == 'doctor' and not field.data:
            raise ValidationError('Latitude is required for doctors.')
        if field.data and not -90 <= float(field.data) <= 90:
            raise ValidationError('Invalid latitude value.')
    
    def validate_longitude(self, field):
        if self.user_type.data == 'doctor' and not field.data:
            raise ValidationError('Longitude is required for doctors.')
        if field.data and not -180 <= float(field.data) <= 180:
            raise ValidationError('Invalid longitude value.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password') 