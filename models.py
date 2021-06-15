from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.Text, primary_key=True, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    user_name = db.Column(db.Text, db.ForeignKey('users.username'))

    user = db.relationship('User', backref="feedbacks")
