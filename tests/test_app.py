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