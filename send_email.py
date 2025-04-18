import smtplib
from email.message import EmailMessage

# Sender email configuration
from_email_addr = "nuist202283890005@163.com"
from_email_pass = "BCNqp7YjdFUZZKYL"
to_email_addr = "nuist202283890005@163.com"

# Create email message object
msg = EmailMessage()

# Set email body content
body = "Hello from Raspberry Pi"
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set email subject
msg['Subject'] = 'TEST EMAIL'

try:
    # Connect to SMTP server (using Gmail as example)
    server = smtplib.SMTP()
    server.connect("smtp.163.com",25)
    # Enable TLS encryption
    #server.starttls()
    
    # Login to email account
    server.login(from_email_addr, from_email_pass)
    
    # Send the email
    server.send_message(msg)
    print('Email sent successfully')
    server.quit()

except Exception as e:
    print(f'Sending failed: {str(e)}')
    server.quit()

