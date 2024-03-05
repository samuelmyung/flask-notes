from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""