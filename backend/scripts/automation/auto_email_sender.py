import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailSender:
    def __init__(self, config_file="email_config.json"):
        self.config = self.load_config(config_file)
    
    def load_config(self, config_file):
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": ""
            }
    
    def send_email(self, recipient, subject, body, attachments=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            
            text = msg.as_string()
            server.sendmail(self.config['sender_email'], recipient, text)
            server.quit()
            
            print(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_bulk_emails(self, recipient_list, subject, body, attachments=None):
        success_count = 0
        for recipient in recipient_list:
            if self.send_email(recipient, subject, body, attachments):
                success_count += 1
        
        print(f"Successfully sent {success_count}/{len(recipient_list)} emails")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python auto_email_sender.py <recipient> <subject> <body> [attachment1] [attachment2]...")
        sys.exit(1)
    
    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) > 4 else None
    
    sender = EmailSender()
    sender.send_email(recipient, subject, body, attachments)
