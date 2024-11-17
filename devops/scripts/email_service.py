import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from logging_config import logger  # Assuming logger is defined in logging_config.py

def send_email(subject, body, to_addresses):
    logger.info(os.getenv("EMAIL_USERNAME"))
    """Send an email notification."""
    from_email = os.getenv("EMAIL_USERNAME")  
    from_password = os.getenv("EMAIL_PASSWORD")  

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_addresses)
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

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
