from models import connect_db, db
from flask import Flask, render_template, flash, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/flask-feedback?user=postgres&password=postgresql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/register')


@app.route('/register')
def user_register():
    form = UserForm()
    return render_template('register.html', form=form)
