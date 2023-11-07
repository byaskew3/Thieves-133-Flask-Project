from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Routing
@app.route('/')
@app.route('/home')
def hello_thieves():
    return '<h1>Hello Thieves, this is flask</h1>'

# Variable Rules
@app.route('/user/<username>')
def show_user(username):
    return f'Hello {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'This is post {post_id}'

# HTTP Methods & Rendering Templates
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Successfully Logged In'
    else:
        return render_template('login.html')

# Showing backend data on the frontend
@app.route('/students')
def students():
    all_students = ['Maria', 'Alicia', 'Anthony']
    return render_template('students.html', all_students=all_students)



# F1 Data
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