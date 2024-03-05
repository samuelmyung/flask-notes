from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


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

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

