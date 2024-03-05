"""Flask app for Notes"""
import os
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

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


# toolbar = DebugToolbarExtension(app)

session_key = "username"


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

        try:
            user = User.register(
                username,
                password,
                email,
                first_name,
                last_name
            )
            db.session.add(user)
            db.session.commit()

            session[session_key] = user.username

            return redirect(f'/users/{username}')

        except IntegrityError:
            flash("Username or email exist")
            return render_template("register.html", form=form)

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs in user and handles login form submission"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.hashed_password.data

        user = User.authenticate(username, password)

        if user:
            session[session_key] = user.username

            return redirect(f'/users/{username}')

        else:
            form.username.errors = ["Invalid name/password"]

    return render_template("login-form.html", form=form)


@app.get("/users/<username>")
def profile_page(username):
    """Shows info about the user"""

    form = CSRFProtectForm()

    user = User.query.get_or_404(username)
    if "username" not in session:
        flash("You must be logged in to view")

        return redirect("/")

    else:
        return render_template("user-info.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs the user out and redirects to the homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')
