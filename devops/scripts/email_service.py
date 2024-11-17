import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header  # Added this import
import os
from logging_config import logger

load_dotenv(dotenv_path=".env.test")

def sanitize_body(body):
    """
    Sanitize the body by handling various Unicode characters.
    Returns a properly encoded string safe for email transmission.
    """
    if not isinstance(body, str):
        body = str(body)
    
    # Replace common problematic characters
    replacements = {
        '\xa0': ' ',  # Replace non-breaking space with regular space
        '\u2018': "'", # Replace left single quotation mark
        '\u2019': "'", # Replace right single quotation mark
        '\u201c': '"', # Replace left double quotation mark
        '\u201d': '"', # Replace right double quotation mark
        '\u2013': '-', # Replace en dash
        '\u2014': '--' # Replace em dash
    }
    
    for old, new in replacements.items():
        body = body.replace(old, new)
    
    return body

def send_email(subject, body, to_addresses):
    """
    Send an email with proper Unicode handling.
    
    Args:
        subject (str): Email subject
        body (str): Email body text
        to_addresses (list): List of recipient email addresses
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    logger.info("Preparing to send email using account: %s", os.getenv("EMAIL_USERNAME"))
    
    # Get credentials from environment
    from_email = os.getenv("EMAIL_USERNAME")
    from_password = os.getenv("EMAIL_PASSWORD")
    
    # Validate environment variables
    if not from_email or not from_password:
        logger.error("Missing EMAIL_USERNAME or EMAIL_PASSWORD in environment variables.")
        return False
    
    try:
        # Create message container with Unicode support
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ", ".join(to_addresses)
        
        # Handle subject encoding - modified to handle Unicode without Header class
        msg['Subject'] = subject
        
        # Sanitize and encode body
        sanitized_body = sanitize_body(body)
        msg.attach(MIMEText(sanitized_body, 'plain', 'utf-8'))
        
        # SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        logger.info("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enable debugging
            server.starttls()  # Enable TLS
            
            # Login
            server.login(from_email, from_password)
            logger.info("Successfully logged in to SMTP server")
            
            # Send email
            server.sendmail(from_email, to_addresses, msg.as_string())
            logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
            
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email: {e}")
        return False

# Example usage
if __name__ == "__main__":
    recipients = ["ayalm13574@gmail.com"]
    subject = "Test Email with Unicode"
    body = "This is a test email with Unicode characters: Hello world! 你好世界！"
    
    success = send_email(subject, body, recipients)
    print(f"Email sent successfully: {success}")