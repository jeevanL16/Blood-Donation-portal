from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class DonorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(),NumberRange(min=18,max=65,message="Age must be beetween 18 and 65")])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'),('Other','Other')])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A-'),('A-','A-'), ('B+', 'B+'),('B-','B-'), ('O+', 'O+'),('O-','O-'), ('AB+', 'AB+'),('AB-','AB-')])
    contact = StringField('Contact', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Register')

class RequestForm(FlaskForm):
    name = StringField('Patient Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
    ], validators=[DataRequired()])
    bloodgroup = SelectField('Blood Group', choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], validators=[DataRequired()])
    
    location = StringField('Location', validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired()])
    reason = StringField('Reason', validators=[DataRequired()])
    hospital = StringField('Hospital Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

