from models import connect_db, db, User
from flask import Flask, render_template, flash, redirect, render_template, session, sessions
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/flask-feedback?user=postgres&password=postgresql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


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
    user = User.query.get_or_404(username)
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/login')

    return render_template('user_page.html', user=user)


@app.route('/logout')
def logout_page():
    session.pop('username')
    flash('Successfully Logout', 'info')
    return redirect('/')
