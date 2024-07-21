# Weatherfy App

This Weather Dashboard application is a Flask-based web application that allows users to search for cities and view current weather conditions. Users can also save their favorite cities and view weather updates on their personalized dashboard. 

### Features

	•	User registration and authentication
	•	Search for weather information by city
	•	View current weather details
	•	Save favorite cities
	•	Remove cities from favorites

### API Information
This app uses Openweather's One Call API and their Geocoding API as well.
One Call API 3.0 - https://openweathermap.org/api/one-call-3
Geocoding API - https://openweathermap.org/api/geocoding-api


## Installation
1. Clone the repo
2. Create and Activate a virtual environment
3. Install required packages - There is a **requirements.txt** file containing all you need.
4. Set up the PostgreSQL database and update the database URI in app.py
5. Initialize database
6. Run app! 


## Application Structure

weather-dashboard/
│
├── app.py              # Main application file
├── models.py           # Database models
├── forms.py            # Form definitions
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   └── search.html
├── static/             # Static files (CSS, JS)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── requirements.txt    # List of dependencies
└── README.md           # Documentation file

## Key Files and Directories

#### app.py

This is the main application file where the Flask app is configured and routes are defined.

	•	Configuration settings are loaded based on the environment (development or testing).
	•	Database and extensions (SQLAlchemy, Bcrypt, LoginManager) are initialized.
	•	Routes are defined for home, dashboard, search, signup, login, logout, get_suggestions, get_weather, favorite, and delete_favorite.

#### models.py

Defines the database models for User and Favorite:

	•	User: Stores user information including username, email, and password.
	•	Favorite: Stores favorite cities for each user including city name, latitude, and longitude.

#### forms.py

Contains form definitions for user registration and login using Flask-WTF.

#### templates/

Contains HTML templates for rendering different pages of the application:

	•	base.html: Base template that other templates extend.
	•	home.html: Homepage template.
	•	dashboard.html: User dashboard showing favorite cities and their weather information.
	•	login.html: User login page.
	•	signup.html: User registration page.
	•	search.html: City search page.

#### static/

Contains static files like CSS and JavaScript:

	•	css/styles.css: Custom styles for the application.
	•	js/scripts.js: JavaScript to handle dynamic functionalities like fetching city suggestions and weather data.

#### requirements.txt

Lists all the Python dependencies required to run the application.

## Usage

#### User Registration and Login

	•	Users can sign up for an account using the /signup route.
	•	Registered users can log in using the /login route.

#### Dashboard

	•	Authenticated users can access their dashboard at /dashboard to view their favorite cities and their current weather conditions.
	•	Users can refresh weather data for their favorite cities and delete cities from their favorites list.

#### City Search and Weather Data

	•	Users can search for cities using the /search route.
	•	The application fetches city suggestions using the OpenWeatherMap Geocoding API.
	•	Users can view current weather data for a selected city and add it to their favorites.

#### API Routes

	•	/get_suggestions: Fetches city suggestions based on user input.
	•	/get_weather: Fetches current weather data for a given city.
	•	/favorite: Adds a city to the user’s favorites.
	•	/delete_favorite: Removes a city from the user’s favorites.

#### Tests Folder Documentation

The `tests` folder contains unit tests for the Weather Dashboard application to ensure that various features and routes work as expected. The tests are written using the `unittest` framework along with `Flask-Testing` to facilitate testing the Flask application. Below is an overview of the test structure and the specific test cases included in `test_app.py`.

##### Test File: `test_app.py`

This file includes a suite of test cases designed to verify the functionality of user authentication, dashboard access, weather data retrieval, and favorite management.