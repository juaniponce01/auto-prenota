import os
import smtplib

class SMTPNotifier:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(self, from_email, to_email, subject, body):
        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.smtp_username, self.smtp_password)
            smtp.sendmail(from_email, to_email, message)
            
            
# Example of usage:
# smtp_server = os.environ['SMTP_SERVER']
# smtp_port = os.environ['SMTP_PORT']
# smtp_username = os.environ['SMTP_USERNAME']
# smtp_password = os.environ['SMTP_PASSWORD']

# notifier = SMTPNotifier(smtp_server, smtp_port, smtp_username, smtp_password)

# from_email = 'juaniponce0@gmail.com'
# to_email = 'juaniponce0@gmail.com'
# subject = 'Hola, mundo!'
# body = 'Este es un mail de prueba.'

# result = notifier.send_email(from_email, to_email, subject, body)
# print(result)

