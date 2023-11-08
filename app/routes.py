from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm

# Home
@app.route('/')
@app.route('/home')
def hello_thieves():
    return render_template('home.html')

REGISTERED_USERS = {
    'dk@thieves.com': {
        'name': 'Dylan Katina',
        'password': 'ilovemydog'
    }
}

#  Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return f'Hello, {REGISTERED_USERS[email]["name"]}'
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)

# F1
@app.route('/f1/driverStandings', methods=['GET', 'POST'])
def get_driver_data_year_rnd():

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