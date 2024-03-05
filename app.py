"""Flask app for Notes"""
import os
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from models import Note, db, connect_db
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