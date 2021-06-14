from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):

    username = StringField(
        "UserName", validators.InputRequired, validators.length(max=20))

    password = PasswordField("Password", validators.InputRequired)

    email = StringField("Email",  validators.InputRequired,
                        validators.length(max=50))

    first_name = StringField(
        "First Name", validators.InputRequired, validators.length(max=20))

    last_name = StringField(
        "Last Name", validators.InputRequired, validators.length(max=20))
