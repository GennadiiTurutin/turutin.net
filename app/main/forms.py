from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import request

class CommentForm(FlaskForm):
    content = TextAreaField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    tag = StringField('Enter tag', validators=[DataRequired()])

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class ProfileForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update My Profile')



