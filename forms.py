from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Form for registration"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    hashed_password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
    )

class LoginForm(FlaskForm):
    """Form for login"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    hashed_password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

