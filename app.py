"""Flask app for Notes"""
import os
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from models import User, db, connect_db
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Redirects to /register"""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers user and handles register form submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.hashed_password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(
            username,
            password,
            email,
            first_name,
            last_name
            )

        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect(f'/users/{username}')

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs in user and handles login form submission"""

    form = LoginForm()
