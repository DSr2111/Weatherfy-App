import os

class Config:
    SECRET_KEY = 'sb123'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sb123@localhost:5432/weather_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False