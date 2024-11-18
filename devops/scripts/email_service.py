import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from logging_config import logger

load_dotenv(dotenv_path=".env.test")


def send_email(subject, body, to_addresses):
    logger.info(os.getenv("EMAIL_USERNAME"))
    """Send an email notification."""
    from_email = os.getenv("EMAIL_USERNAME")
    from_password = os.getenv("EMAIL_PASSWORD")

    # Path to the log file
    log_file_path = os.path.join(os.path.dirname(__file__), 'logs', 'ci_pipeline.log')

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_addresses)
    msg['Subject'] = subject

    # Attach the body to the email with UTF-8 encoding
    msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

    # Attach the log file
    try:
        with open(log_file_path, "rb") as log_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(log_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='ci_pipeline.log')
            msg.attach(part)
    except Exception as e:
        logger.error(f"Failed to attach log file: {e}")

    # SMTP server configuration (e.g., Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        logger.info("Connecting to SMTP server...")
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, from_password)
            logger.info(f"Logged in to the SMTP server with {from_email}")
            server.sendmail(from_email, to_addresses, msg.as_string())
        logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
