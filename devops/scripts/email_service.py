import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
import os

load_dotenv(dotenv_path=".env.test")
def send_email(subject, body, to_addresses):
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
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, from_password)
            server.sendmail(from_email, to_addresses, msg.as_string())
        print(f"Email sent successfully to {', '.join(to_addresses)}")
    except Exception as e:
        print(f"Failed to send email: {e}")