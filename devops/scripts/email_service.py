import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from logging_config import logger

load_dotenv(dotenv_path=".env.test")

def sanitize_body(body):
    """
    Convert body to string and replace problematic characters.
    """
    # First ensure we're working with a string
    body = str(body)
    
    try:
        # Try to encode and decode to catch any encoding issues early
        return body.encode('utf-8').decode('utf-8')
    except UnicodeError:
        # If there are encoding issues, do character replacement
        replacements = {
            '\xa0': ' ',
            '\u2018': "'",
            '\u2019': "'",
            '\u201c': '"',
            '\u201d': '"',
            '\u2013': '-',
            '\u2014': '--'
        }
        for old, new in replacements.items():
            body = body.replace(old, new)
        return body

def send_email(subject, body, to_addresses):
    """
    Send an email with UTF-8 encoding throughout.
    """
    logger.info("Preparing to send email using account: %s", os.getenv("EMAIL_USERNAME"))
    
    from_email = os.getenv("EMAIL_USERNAME")
    from_password = os.getenv("EMAIL_PASSWORD")
    
    if not from_email or not from_password:
        logger.error("Missing EMAIL_USERNAME or EMAIL_PASSWORD in environment variables.")
        return False
    
    try:
        # Create the message container - using UTF-8 encoding
        msg = MIMEMultipart('alternative')
        
        # Encode the subject
        subject = sanitize_body(subject)
        msg['Subject'] = subject
        
        # Encode the addresses
        msg['From'] = formataddr(('', from_email))
        msg['To'] = ', '.join(formataddr(('', addr.strip())) for addr in to_addresses)
        
        # Sanitize and encode the body
        sanitized_body = sanitize_body(body)
        
        # Create both plain text part
        text_part = MIMEText(sanitized_body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        logger.info("Connecting to SMTP server...")
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)
            server.starttls()
            
            try:
                server.login(from_email, from_password)
                logger.info("Successfully logged in to SMTP server")
                
                # Convert the entire message to a string with proper encoding
                email_message = msg.as_string()
                
                # Send the email
                server.sendmail(from_email, to_addresses, email_message)
                logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"Authentication failed: {e}")
                return False
                
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return False
    except UnicodeEncodeError as e:
        logger.error(f"Unicode encoding error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email: {e}")
        return False

# Example usage
if __name__ == "__main__":
    try:
        recipients = ["example@example.com"]
        subject = "Test Email with Unicode"
        body = "This is a test email with Unicode characters: Hello world! 你好世界！"
        
        success = send_email(subject, body, recipients)
        print(f"Email sent successfully: {success}")
    except Exception as e:
        print(f"Error in main: {e}")