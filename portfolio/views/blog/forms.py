import datetime

from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


def get_date():
    return 'date: ' + datetime.datetime.today().strftime('%Y-%m-%d')


class AddPostForm(FlaskForm):
    blog_title = TextField('bolg_title', validators=[DataRequired(), Length(min=6,)])
    # blog_date = DateField('blog_date', validators=[DataRequired()])
    blog_body = TextAreaField('post_body', validators=[DataRequired(), Length(min=6,)], default=get_date())


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
