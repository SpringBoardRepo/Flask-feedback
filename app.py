from flask_wtf import form
from models import Feedback, connect_db, db, User
from flask import Flask, render_template, flash, redirect, render_template, session, sessions
from flask_debugtoolbar import DebugToolbarExtension
from forms import FeedbackForm, UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECERT_KEY', "oh-so-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', "postgresql://localhost/flask-feedback?user=postgres&password=postgresql")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)

        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back!!! {user.username}', 'success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid usename/password']

    return render_template('login.html', form=form)


@app.route('/users/<string:username>')
def user_page(username):

    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/login')

    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.all()
    return render_template('user_page.html', user=user, feedbacks=feedbacks)


@app.route('/logout')
def logout_page():
    session.pop('username')
    flash('Successfully Logout', 'info')
    return redirect('/')


@app.route('/<string:username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    form = FeedbackForm()

    if 'username' not in session:
        flash(f'Please login!!!', 'danger')
        return redirect('/login')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content,
                            user_name=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback.html', form=form)


@app.route('/feedback/<int:id>/edit', methods=['GET', 'POST'])
def edit_feedback(id):
    feedback = Feedback.query.get_or_404(id)

    form = FeedbackForm(obj=feedback)
    if 'username' not in session:
        flash('Please login First!!', 'danger')
        return redirect('/login')
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.user_name}')

    return render_template('feedback.html', form=form)


@app.route('/feedback/<int:id>/delete')
def delete_feedback(id):

    feedback = Feedback.query.get_or_404(id)
    if feedback.user_name == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback Deleted', 'info')
        return redirect(f'/users/{feedback.user_name}')

    flash('You can not delete this feedback', 'info')
    return redirect(f'/users/{feedback.user_name}')


@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):

    user = User.query.get_or_404(username)
    if user.username == session['username']:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('Account Deleted', 'warning')
        return redirect('/register')
    flash('You can not delete this Account', 'info')
    return redirect(f'/users/{user.username}')
