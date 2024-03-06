"""Flask app for Notes"""
import os
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

from models import User, Note, db, connect_db
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, UpdateNoteForm

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
    notes = user.notes

    if "username" not in session:
        flash("You must be logged in to view")

        return redirect("/")

    elif username != session[session_key]:

        flash("You must be logged in to view")

        return redirect(f"/users/{session[session_key]}")

    else:

        return render_template("user-info.html", user=user, form=form, notes=notes)


@app.post("/logout")
def logout():
    """Logs the user out and redirects to the homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')


@app.post("/users/<username>/delete")
def delete_user(username):
    """Deletes the user from the database"""

    user = User.query.get_or_404(username)

    if username == session[session_key]:
        for note in user.notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        form = CSRFProtectForm()

        if form.validate_on_submit():
            session.pop("username", None)

        return redirect("/")

    else:
        flash("You must be logged in to view")

        return redirect(f"/users/{session[session_key]}")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    """Shows form for adding notes and handles the form submission"""

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner_username=username)

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:

        return render_template("add-note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def edit_notes(note_id):
    """Show form for editing notes and handles the form submission"""

    note = Note.query.get_or_404(note_id)

    if note.owner_username == session[session_key]:
        form = UpdateNoteForm(obj=note)

        if form.validate_on_submit():
            note.title = form.title.data or note.title
            note.content = form.content.data or note.content

            db.session.commit()

            return redirect(f'/users/{note.owner_username}')

        else:
            return render_template("edit-note.html", form=form, note=note)

    else:
        flash("You must be logged in to view")

        return redirect(f"/users/{session[session_key]}")

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes the note and redirects to the user page"""

    note = Note.query.get_or_404(note_id)

    if note.owner_username == session[session_key]:

        db.session.delete(note)
        db.session.commit()

        return redirect(f'/users/{note.owner_username}')

    else:
        flash("You must be logged in to view")

        return redirect(f"/users/{session[session_key]}")
