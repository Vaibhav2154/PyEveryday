import smtplib
from email.message import EmailMessage

# --- Configuration ---
EMAIL_ADDRESS = 'vaibhavvaibhu2005@gmail.com'       # Replace with your email
EMAIL_PASSWORD = ''         # App password or actual password
SUBJECT = 'ED team interview schedule'
TEST_LINK = 'https://docs.google.com/spreadsheets/d/1z66pPR8mJHoS9kwVTXpJRIHgvHAea9Dsy6QuusJHCnc/edit?gid=0#gid=00'
with open('emails.txt', 'r') as file:
    recipients = [line.strip() for line in file if line.strip()]

body = f"""
Hello,

This is an automated email.
Please find the interview schedule for the Student coordination team at the following link:
{TEST_LINK}

Regards,
Linux Campus Club
JSSSTU, Mysuru
"""

# --- Create the email ---
msg = EmailMessage()
msg['From'] = EMAIL_ADDRESS
msg['Subject'] = SUBJECT
msg.set_content(body)

# --- Send email to each recipient ---
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    for recipient in recipients:
        msg['To'] = recipient
        smtp.send_message(msg)
        print(f'Email sent to {recipient}')
        del msg['To']  # Remove 'To' header before next iteration
