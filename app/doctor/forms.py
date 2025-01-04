from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app.models import User
from flask_login import current_user

class ScheduleForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Schedule')

class ReferralForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    referred_doctor_id = SelectField('Refer To', coerce=int, validators=[DataRequired()])
    reason = TextAreaField('Reason for Referral', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes')
    submit = SubmitField('Create Referral')

    def __init__(self, *args, **kwargs):
        super(ReferralForm, self).__init__(*args, **kwargs)
        # Get all doctors except the current one
        doctors = User.query.filter(
            User.user_type == 'doctor',
            User.id != current_user.id
        ).all()
        self.referred_doctor_id.choices = [(d.id, f"Dr. {d.username} ({d.specialization})") for d in doctors]
        self.patient_id.choices = [
            (p.id, f"{p.username} ({p.email})")
            for p in User.query.filter_by(user_type='patient').all()
        ] 