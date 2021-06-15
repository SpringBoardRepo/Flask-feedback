from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, Length


class UserForm(FlaskForm):

    username = StringField(
        "UserName", validators=[validators.InputRequired(), validators.Length(max=20)])

    password = PasswordField("Password", validators=[
                             validators.InputRequired()])

    email = StringField("Email",  validators=[validators.InputRequired(),
                                              validators.Length(max=50)])

    first_name = StringField(
        "First Name", validators=[validators.InputRequired(), validators.Length(max=20)])

    last_name = StringField(
        "Last Name", validators=[validators.InputRequired(), validators.Length(max=20)])


class LoginForm(FlaskForm):

    username = StringField("UserName", validators=[validators.InputRequired()])

    password = PasswordField("Password", validators=[
                             validators.InputRequired()])


class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[
                        validators.InputRequired(), validators.Length(max=100)])

    content = StringField("Content", validators=[validators.InputRequired()])
