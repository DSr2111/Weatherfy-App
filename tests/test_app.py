import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, User, Favorite

class BaseTestCase(TestCase):
    """Base test case for setting up the Flask app and database for testing."""
    
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'test_secret'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """Set up a blank database before each test."""
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        """Destroy the database after each test."""
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        """Create a test user."""
        user = User(username='testuser', email='testuser@example.com', password='password')
        db.session.add(user)
        db.session.commit()

#Authentication tests
class TestUserAuthentication(BaseTestCase):
    """Test cases for user authentication routes."""

    def test_signup(self):
        """Test user signup."""
        response = self.client.post('/signup', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup successful! You are now logged in.', response.data)
    
    def test_signup_invalid_data(self):
        """Test user signup with invalid data."""
        # Test missing password confirmation
        response = self.client.post('/signup', data={
            'username': 'invaliduser',
            'email': 'invaliduser@example.com',
            'password': 'password123',
            'confirm_password': ''  # Missing confirmation
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error in the Confirm Password field - This field is required.', response.data)
        
        # Test mismatched passwords
        response = self.client.post('/signup', data={
            'username': 'mismatchuser',
            'email': 'mismatchuser@example.com',
            'password': 'password123',
            'confirm_password': 'password321'  # Mismatch
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error in the Confirm Password field - Passwords must match.', response.data)
        
        # Test missing username
        response = self.client.post('/signup', data={
            'username': '',
            'email': 'nouser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error in the Username field - This field is required.', response.data)

    def test_login(self):
        """Test user login."""
        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credentials valid and login successful!', response.data)

    def test_logout(self):
        """Test user logout."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_login_invalid_data(self):
        """Test user login with invalid data."""
        # Test incorrect password
        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credentials invalid. Please review email and password.', response.data)
        
        # Test non-existent email
        response = self.client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credentials invalid. Please review email and password.', response.data)

#Dashboard tests
class TestDashboard(BaseTestCase):
    """Test cases for the dashboard route."""

    def test_dashboard_access(self):
        """Test access to the dashboard."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Dashboard', response.data)

# Weather Routes tests
class TestWeatherRoutes(BaseTestCase):
    """Test cases for weather-related routes."""

    def test_get_suggestions(self):
        """Test city suggestions."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        response = self.client.get('/get_suggestions?query=London')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'London', response.data)

    def test_get_weather(self):
        """Test weather data retrieval."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        response = self.client.get('/get_weather?lat=51.51&lon=-0.13&city_name=London')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'temperature', response.data)
    
    def test_get_weather_invalid_query(self):
        """Test weather data retrieval with invalid query parameters."""
        # Test missing lat and lon
        response = self.client.get('/get_weather?city_name=London')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Error: Latitude and longitude are required.', response.data)
        
        # Test invalid latitude and longitude
        response = self.client.get('/get_weather?lat=abc&lon=xyz&city_name=London')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Error: Invalid latitude or longitude.', response.data)
        
        # Test city name with no matching weather data
        response = self.client.get('/get_weather?lat=1000&lon=1000&city_name=InvalidCity')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Weather data not found', response.data)

class TestFavoriteRoutes(BaseTestCase):
    """Test cases for favorite management routes."""

    def test_add_favorite(self):
        """Test adding a city to favorites."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        response = self.client.post('/favorite', json={
            'city_name': 'London',
            'lat': '51.51',
            'lon': '-0.13'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_delete_favorite(self):
        """Test deleting a city from favorites."""
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        # First add a favorite to delete
        self.client.post('/favorite', json={
            'city_name': 'London',
            'lat': '51.51',
            'lon': '-0.13'
        })
        response = self.client.post('/delete_favorite', json={'city_name': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
    

if __name__ == '__main__':
    unittest.main()