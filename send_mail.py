import smtplib
from email.mime.text import MIMEText # allows to send text in HTML emails

def send_mail(customer, agent, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'ecaa64dc2e7698'
    password = '00f9c25a392c98'
    message = f'<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Agent: {agent}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>'

    sender_email = 'email1@example.com'
    receiver_email = 'regina.liuyixuan@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Funk Travels Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())