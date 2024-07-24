import os

class Config:
    SECRET_KEY = 'sb123'
    SQLALCHEMY_DATABASE_URI = 'postgresql://dsr:Lss4SfvWTPJl8JEkTMGw5ChzJBoom5Df@dpg-cqgnr8lds78s73bjg9ug-a.oregon-postgres.render.com/weather_db_ocxr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False