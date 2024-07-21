-- Create the weather_db database if it doesn't exist
CREATE DATABASE IF NOT EXISTS weather_db;

-- Connect to the weather_db database
\c weather_db;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE -- Added the is_active column
);

-- Create the favorites table
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(150) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL
);