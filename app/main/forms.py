from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class CommentForm(FlaskForm):
    content = TextAreaField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    tag = StringField('Enter tag', validators=[DataRequired()])

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    change_password = SubmitField('Change password')
    submit = SubmitField('Update My Profile')