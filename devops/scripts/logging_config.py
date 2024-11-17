import logging
from logging.handlers import SysLogHandler
import os
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

    # Splunk SysLogHandler
    splunk_handler = SysLogHandler(address=('splunk', 8088))  # Replace 'splunk' with Splunk container IP/hostname
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