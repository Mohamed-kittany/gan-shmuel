import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from logging_config import logger

load_dotenv(dotenv_path=".env.test")

def send_email(subject, body, to_addresses):
    logger.info("email: %s", os.getenv("EMAIL_USERNAME"))
    from_email = os.getenv("EMAIL_USERNAME")
    from_password = os.getenv("EMAIL_PASSWORD")

    # Check if the environment variables are missing
    if not from_email or not from_password:
        logger.error("Missing EMAIL_USERNAME or EMAIL_PASSWORD in environment variables.")
        return

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_addresses)
    msg['Subject'] = subject

    # Attach the body to the email with UTF-8 encoding
    msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

    # SMTP server configuration (e.g., Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        logger.info("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enable SMTP debugging for detailed logs
            server.starttls()  # Secure the connection
            server.login(from_email, from_password)
            logger.info(f"Logged in to the SMTP server with {from_email}")
            server.sendmail(from_email, to_addresses, msg.as_string())
        logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
