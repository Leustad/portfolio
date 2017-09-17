from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class AddPostForm(FlaskForm):
    blog_title = StringField('bolg_title', validators=[DataRequired(), Length(min=6,)])
    blog_body = TextAreaField('post_body', validators=[DataRequired(), Length(min=6,)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
