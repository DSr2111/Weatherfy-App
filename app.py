from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
import requests
from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from models import db, User, Favorite
from forms import RegistrationForm, LoginForm
from config import Config, TestConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

flask_env = os.getenv('FLASK_ENV', 'development')
if flask_env == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#API Key for OpenWeather
api_key = os.getenv('API_KEY')

@app.route('/')
def home():
    styles = "css/styles.css"
    return render_template('home.html', styles=styles)


@app.route('/dashboard')
@login_required
def dashboard():
    user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', favorites=user_favorites, user_name=current_user.username)


@app.route('/search', methods=['GET'])
@login_required
def search():
    return render_template('search.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)  # Log the user in after successful signup
        flash('Signup successful! You are now logged in.', 'success')
        return redirect(url_for('login'))  
    else:
        flash_errors(form)  # Flash form errors if validation fails
    return render_template('signup.html', form=form)

def flash_errors(form):
    """Flashes form errors."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Credentials valid and login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credentials invalid. Please review email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Need to use Geocoding API for cities
# this brings back longitude and latitude coordinates
@app.route('/get_suggestions', methods=['GET'])
@login_required
def get_suggestions():
    query = request.args.get('query')
    if query:
        suggestions_url = f'http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}'
        response = requests.get(suggestions_url)
        suggestions = response.json()
        
        results = []
        for suggestion in suggestions:
            results.append({
                'name': suggestion['name'],
                'lat': suggestion['lat'],
                'lon': suggestion['lon'],
                'country': suggestion.get('country', ''),
                'state': suggestion.get('state', '')
            })
        return jsonify(results)
    return jsonify([])

@app.route('/get_weather', methods=['GET'])
@login_required
def get_weather():
    city_name = request.args.get('city_name')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric'
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if 'current' in weather_data:
        weather = {
            'name': city_name,
            'temp': weather_data['current']['temp'],
            'description': weather_data['current']['weather'][0]['description'],
            'icon': weather_data['current']['weather'][0]['icon'],
            'lat': lat,
            'lon': lon
        }
        return jsonify(weather)
    else:
        print(weather_data)
        return jsonify({'error': 'Weather data not found'})

@app.route('/favorite', methods=['POST'])
@login_required
def favorite():
    data = request.get_json()
    city_name = data.get('city_name')
    lat = data.get('lat')
    lon = data.get('lon')
    if city_name and lat and lon:
        existing_favorite = Favorite.query.filter_by(user_id=current_user.id, city_name=city_name).first()
        if not existing_favorite:
            new_favorite = Favorite(city_name=city_name, user_id=current_user.id, lat=lat, lon=lon)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'info', 'message': f'{city_name} is already in your favorites.'})
    return jsonify({'status': 'error', 'message': 'City name, latitude, and longitude are required.'})


@app.route('/delete_favorite', methods=['POST'])
@login_required
def delete_favorite():
    data = request.get_json()
    city_name = data.get('city_name')
    print(f"Delete request received for {city_name}")  # Log the request
    if city_name:
        favorite = Favorite.query.filter_by(user_id=current_user.id, city_name=city_name).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            print(f"Deleted favorite: {city_name}")  # Confirm deletion
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Favorite not found.'})
    return jsonify({'status': 'error', 'message': 'City name is required.'})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)