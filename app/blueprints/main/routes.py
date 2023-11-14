from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required
import requests


# Home
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')



# F1
@main.route('/f1/driverStandings', methods=['GET', 'POST'])
@login_required
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