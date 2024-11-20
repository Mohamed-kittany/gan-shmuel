# # app/extensions.py
# import os
# import logging
# import mysql.connector # type: ignore
# from logging.handlers import RotatingFileHandler
# from app.config import config

# # Initialize MySQL connection using Flask config
# def get_mysql_connection():
#     """
#     Returns a new MySQL connection using the app's configuration.
#     """
#     return mysql.connector.connect(
#         host=config['MYSQL_DATABASE_HOST'],
#         user=config['MYSQL_DATABASE_USER'],
#         password=config['MYSQL_DATABASE_PASSWORD'],
#         database=config['MYSQL_DATABASE_DB']
#     )

# # Logging configuration
# def configure_logging(app):
#     """
#     Configures logging for the Flask app.
#     Logs are written only to a rotating log file.
#     """
#     # Create a logs directory if it doesn't exist
#     log_dir = os.path.join(os.getcwd(), 'logs')
#     os.makedirs(log_dir, exist_ok=True)
#     log_file = os.path.join(log_dir, 'api.log')

#     # Formatter for logs
#     formatter = logging.Formatter(
#         '[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s'
#     )

#     # File handler with rotation. Each log file is capped at 10MB. Keeps up to 5 old log files.
#     file_handler = RotatingFileHandler(
#         log_file, maxBytes=10 * 1024 * 1024, backupCount=5
#     )
#     file_handler.setLevel(logging.INFO)
#     file_handler.setFormatter(formatter)

#     # Add the file handler to the Flask app logger
#     app.logger.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)

#     # Log a startup message
#     app.logger.info("Logging is configured")


import os
import logging
import mysql.connector # type: ignore
from logging.handlers import RotatingFileHandler, HTTPHandler
import json
import urllib.request
from urllib.error import URLError, HTTPError
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
    Logs are written to a rotating log file and sent to Splunk.
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

    # Splunk HTTP Handler
    class SplunkHttpHandler(HTTPHandler):
        def __init__(self, splunk_url, token):
            # Set up Splunk HEC URL and token
            self.splunk_url = splunk_url
            self.token = token
            # Initialize HTTPHandler with Splunk's HEC URL
            super().__init__(splunk_url, '/services/collector/event', method='POST')

        def emit(self, record):
            # Create the log entry in JSON format
            log_entry = self.format(record)
            payload = {
                "event": log_entry,
                "sourcetype": "docker",  
                "index": "main",       
            }

            headers = {
                "Authorization": f"Splunk {self.token}",
                "Content-Type": "application/json",
            }

            # Send the log to Splunk HEC via HTTP POST request
            try:
                req = urllib.request.Request(
                    self.splunk_url + '/services/collector/event', 
                    data=json.dumps(payload).encode('utf-8'),
                    headers=headers
                )
                urllib.request.urlopen(req)
            except HTTPError as e:
                print(f"HTTPError: {e.code} - {e.reason}")
            except URLError as e:
                print(f"URLError: {e.reason}")

    # Add the Splunk HTTP Handler if Splunk URL and token are available
    splunk_url = config.get("SPLUNK_URL", "http://splunk:8088")  # Update with your Splunk HEC URL
    splunk_token = config.get("SPLUNK_TOKEN", "f304dc24-869b-4907-a3bf-6d47f9f8d1bf")  # Update with your HEC token
    if splunk_url and splunk_token:
        splunk_handler = SplunkHttpHandler(splunk_url, splunk_token)
        splunk_handler.setFormatter(formatter)
        splunk_handler.setLevel(logging.INFO)
    else:
        splunk_handler = None

    # Set up the Flask app logger
    app.logger.setLevel(logging.INFO)

    # Add log handlers
    app.logger.addHandler(file_handler)
    if splunk_handler:
        app.logger.addHandler(splunk_handler)

    # Log a startup message
    app.logger.info("Logging is configured")

