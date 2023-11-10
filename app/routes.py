from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

# Home
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#  Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data 
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        # Create an instance of our User Class
        user = User(first_name, last_name, email, password)

        # add user to database
        db.session.add(user)
        db.session.commit()

        flash(f'Thank you for signing up {first_name}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('login'))

# F1
@app.route('/f1/driverStandings', methods=['GET', 'POST'])
def driver_standings():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')

        url = f'https://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        try:
            new_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            # call helper function
            all_drivers = get_driver_data(new_data)
            return render_template('driverStandings.html', all_drivers=all_drivers)
        except IndexError:
            return 'Invalid round or year'
    else:
        return render_template('driverStandings.html')

def get_driver_data(data):
    new_driver_data = []
    for driver in data:
        driver_dict = {
            'first_name': driver['Driver']['givenName'],
            'last_name': driver['Driver']['familyName'],
            'DOB': driver['Driver']['dateOfBirth'],
            'wins': driver['wins'],
            'team': driver['Constructors'][0]['name']
        }
        new_driver_data.append(driver_dict)
    return new_driver_data