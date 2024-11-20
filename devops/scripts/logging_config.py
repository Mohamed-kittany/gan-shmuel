import logging
from logging.handlers import HTTPHandler
import os
import json
import urllib.request
from urllib.error import URLError, HTTPError

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

def setup_logging():
    logger = logging.getLogger('ci_pipeline')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # File Handler
    log_file = os.path.join(os.path.dirname(__file__), 'logs', 'ci_pipeline.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Splunk HTTP Handler
    splunk_url = "http://splunk:8088"  # Replace with your Splunk HEC endpoint
    splunk_token = "f304dc24-869b-4907-a3bf-6d47f9f8d1bf"  # Replace with your HEC token
    splunk_handler = SplunkHttpHandler(splunk_url, splunk_token)
    splunk_handler.setFormatter(formatter)
    splunk_handler.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(splunk_handler)

    logger.propagate = False
    return logger

logger = setup_logging()
