# app/extensions.py
import os
import logging
import mysql.connector # type: ignore
from logging.handlers import RotatingFileHandler
from app.config import config

# Initialize MySQL connection using Flask config
def get_mysql_connection():
    """
    Returns a new MySQL connection using the app's configuration.
    """
    return mysql.connector.connect(
        host=config['MYSQL_DATABASE_HOST'],
        user=config['MYSQL_DATABASE_USER'],
        password=config['MYSQL_DATABASE_PASSWORD'],
        database=config['MYSQL_DATABASE_DB']
    )

# Logging configuration
def configure_logging(app):
    """
    Configures logging for the Flask app.
    Logs are written only to a rotating log file.
    """
    # Create a logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'api.log')

    # Formatter for logs
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s'
    )

    # File handler with rotation. Each log file is capped at 10MB. Keeps up to 5 old log files.
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add the file handler to the Flask app logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Log a startup message
    app.logger.info("Logging is configured")
