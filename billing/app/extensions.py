# app/extensions.py
import logging
import mysql.connector
from flask import current_app

# Initialize MySQL connection using Flask config
def get_mysql_connection():
    print("123")
    print(current_app.config['MYSQL_DATABASE_USER'])
    return mysql.connector.connect(
        host=current_app.config['MYSQL_DATABASE_HOST'],
        user=current_app.config['MYSQL_DATABASE_USER'],
        password=current_app.config['MYSQL_DATABASE_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE_DB']
        
    )

# Logging configuration
def configure_logging(app):
    handler = logging.FileHandler('api.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
