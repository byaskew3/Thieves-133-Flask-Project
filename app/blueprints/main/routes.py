from app.blueprints.main import main
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, db
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

@main.route('/users')
@login_required
def users():
    all_users = User.query.filter( User.id != current_user.id).all()
    return render_template('users.html', all_users=all_users)

@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.following.append(user)
        db.session.commit()
        flash(f"You are now following {user.first_name} {user.last_name}!", 'info')
    return redirect(url_for('main.users'))

@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user and user in current_user.following:
        current_user.following.remove(user)
        db.session.commit()
        flash(f"You have unfollowed {user.first_name} {user.last_name}!", 'warning')
    return redirect(url_for('main.users'))