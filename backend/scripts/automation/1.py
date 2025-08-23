import smtplib
from email.message import EmailMessage

# --- Configuration ---
EMAIL_ADDRESS = 'vaibhavvaibhu2005@gmail.com'       # Replace with your email
EMAIL_PASSWORD = ''         # App password or actual password
SUBJECT = 'Thank You & Welcome to the Advisory Team - Linux Campus Club (LCC)'

# TODO: Update the advisory role below if needed
ADVISORY_ROLE = 'Advisory Team'  # Can be customized if there are specific advisory positions

with open('emails.txt', 'r') as file:
    recipients = [line.strip() for line in file if line.strip()]

body = f"""
Hello,

Thank you for your incredible dedication! 🎉

We are delighted to inform you that you will be continuing with the Linux Campus Club (LCC) as a valued member of our {ADVISORY_ROLE}.

Your experience, knowledge, and contributions have been invaluable to our club, and we are excited to have you guide and mentor the next generation of tech enthusiasts in this new capacity.


Next Steps:
📅 Advisory Team Meeting: We will be organizing a meeting with all advisory team members to discuss your new role, responsibilities, and how we can work together to make LCC even better. Details will be shared soon.

📱 WhatsApp Group: Please stay connected with our official WhatsApp group for ongoing coordination and updates:
🔗 WhatsApp Group Link: 

The advisory team meeting details including date, time, and venue/platform will be shared with you soon. Please keep an eye on your email and our official communication channels for further updates.

Thank you once again for choosing to stay with LCC and for your commitment to nurturing the next generation of tech enthusiasts. Your continued involvement means a lot to us and to the future members who will benefit from your guidance.

Best regards,
Linux Campus Club (LCC)
JSSSTU, Mysuru

---
For any queries, feel free to reach out to us.
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
