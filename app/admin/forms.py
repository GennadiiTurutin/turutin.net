from flask_wtf import Form
from wtforms.fields import PasswordField, StringField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, DataRequired 

class NewPost(Form):
    title = StringField('Title', validators=[InputRequired()])
    subtitle = StringField('Subtitle', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])
    author = EmailField('Author', validators=[InputRequired()])
    submit = SubmitField('Publish post')

class EditPost(NewPost):
    submit = SubmitField('Edit post')

class EditUser(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

