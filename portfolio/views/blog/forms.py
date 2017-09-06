from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField


class AddPostForm(FlaskForm):
    test = TextAreaField('post', validators=[DataRequired(), Length(min=6,)])
