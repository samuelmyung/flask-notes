"""Models for Note app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    hashed_password = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with all info and return user"""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(
            username=username,
            hashed_password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """ Validate that user exists and password is correct. Return user
        if valid; else return False."""

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.hashed_password, pwd):

            return u
        else:
            return False


class Note(db.Model):
    """Note"""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text(),
        nullable=False
    )

    owner_username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False,
    )

    user = db.relationship('User', backref='notes')
