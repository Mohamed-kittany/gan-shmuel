# app/extensions.py
import logging
import mysql.connector
from flask import current_app
from dotenv import load_dotenv, find_dotenv
import os
#load environment variables from .env file
load_dotenv(find_dotenv())

config = {
    "SECRET_KEY": os.getenv("SECRET_KEY", "your_secret_key"),
    "MYSQL_DATABASE_HOST": os.getenv("MYSQL_DATABASE_HOST", "localhost"),
    "MYSQL_DATABASE_USER": os.getenv("MYSQL_DATABASE_USER", "root"),
    "MYSQL_DATABASE_PASSWORD": os.getenv("MYSQL_DATABASE_PASSWORD", "root"),
    "MYSQL_DATABASE_DB": os.getenv("MYSQL_DATABASE_DB", "billdb"),
}

# Initialize MySQL connection using Flask config
def get_mysql_connection():
    print("123")
    print(current_app.config['MYSQL_DATABASE_USER'])
    return mysql.connector.connect(
        host=config['MYSQL_DATABASE_HOST'],
        user=config['MYSQL_DATABASE_USER'],
        password=config['MYSQL_DATABASE_PASSWORD'],
        database=config['MYSQL_DATABASE_DB']
        
    )

# Logging configuration
def configure_logging(app):
    handler = logging.FileHandler('api.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
