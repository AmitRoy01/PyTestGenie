"""
Email Service
Handles sending emails for password reset and other notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
import string


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.sender_email = os.getenv('SENDER_EMAIL', self.smtp_username)
        self.sender_name = os.getenv('SENDER_NAME', 'PyTestGenie')
        
    @staticmethod
    def generate_reset_code(length: int = 6) -> str:
        """
        Generate a random numeric code for password reset
        
        Args:
            length: Length of the code (default: 6)
        
        Returns:
            Numeric code as string
        """
        return ''.join(random.choices(string.digits, k=length))
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = True) -> tuple[bool, str]:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML (default: True)
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if email is configured
            if not self.smtp_username or not self.smtp_password:
                # For development/testing, just print the email
                print(f"\n{'='*60}")
                print(f"EMAIL SIMULATION (Configure SMTP to send real emails)")
                print(f"{'='*60}")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"Body:\n{body}")
                print(f"{'='*60}\n")
                return True, "Email sent (simulated - configure SMTP for real emails)"
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.sender_name} <{self.sender_email}>"
            message['To'] = to_email
            
            # Attach body
            mime_type = 'html' if is_html else 'plain'
            message.attach(MIMEText(body, mime_type))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            return True, "Email sent successfully"
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return False, f"Failed to send email: {str(e)}"
    
    def send_password_reset_email(self, to_email: str, username: str, reset_code: str) -> tuple[bool, str]:
        """
        Send password reset code email
        
        Args:
            to_email: User's email address
            username: User's username
            reset_code: Generated reset code
        
        Returns:
            Tuple of (success, message)
        """
        subject = "Password Reset Code - PyTestGenie"
        
        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .code-box {{
                    background: white;
                    border: 2px solid #667eea;
                    border-radius: 5px;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                    letter-spacing: 5px;
                }}
                .warning {{
                    color: #e74c3c;
                    font-size: 14px;
                    margin-top: 20px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #777;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 PyTestGenie</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Hello, {username}!</h2>
                    <p>We received a request to reset your password. Use the code below to complete the password reset process:</p>
                    
                    <div class="code-box">
                        <p style="margin: 0; color: #666; font-size: 14px;">Your Reset Code</p>
                        <div class="code">{reset_code}</div>
                    </div>
                    
                    <p>This code will expire in <strong>15 minutes</strong>.</p>
                    
                    <p class="warning">
                        ⚠️ If you didn't request this password reset, please ignore this email or contact support if you have concerns.
                    </p>
                </div>
                <div class="footer">
                    <p>This is an automated message from PyTestGenie. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
