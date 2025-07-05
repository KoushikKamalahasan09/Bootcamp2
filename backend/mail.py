import smtplib

from email.mime.text import MIMEText

SHIP_HOST='localhost'
SHIP_PORT=1025
FROM_EMAIL='admin@admin.com'

def send_mail(to_email, subject, body):
    """
    Sends an email using the SMTP protocol.
    
    :param to_email: Recipient's email address
    :param subject: Subject of the email
    :param body: Body content of the email
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SHIP_HOST, SHIP_PORT) as server:
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}") 