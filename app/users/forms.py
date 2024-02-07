from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired()])
    lastname = StringField('Last Name',
                           validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    phonenumber = IntegerField('Phone Number',
                               validators=[DataRequired(), NumberRange(min=1000000000, max=999999999999999, message="please enter a valid phone number")])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="you password must be atleast 8 characters")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class SignInForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired()])
    lastname = StringField('Last Name',
                           validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    phonenumber = IntegerField('Phone Number',
                           validators=[DataRequired(), NumberRange(min=1000000000, max=999999999999999, message='please enter a valid phone number')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')