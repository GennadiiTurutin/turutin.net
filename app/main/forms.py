from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    tag = StringField('Enter tag', validators=[DataRequired()])