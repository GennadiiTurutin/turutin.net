from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import request

class CommentForm(FlaskForm):
    content = TextAreaField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    tag = StringField('Enter tag', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update My Profile')


class ContactForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Enter your message', validators=[DataRequired()])
    submit = SubmitField('Send a message')


