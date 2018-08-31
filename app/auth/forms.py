from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User 


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirmation = PasswordField('Confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        form = RegistrationForm()
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        form = RegistrationForm()
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None: 
            raise ValidationError('Please use a different email')

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Current password', validators=[DataRequired()])
    newpassword = PasswordField('New password', validators=[DataRequired(), Length(min=6, max=25)])
    confirmation = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Change password')  

class ForgotPasswordForm(FlaskForm):
    newpassword = PasswordField('New password', validators=[DataRequired()])
    confirmation = PasswordField('Confirm new password', validators=[DataRequired(), Length(min=6, max=25)])
    submit = SubmitField('Change password')  

class RequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request link')




