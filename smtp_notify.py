import smtplib

class SMTPNotifier:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(self, from_email, to_email, subject, body):
        message = f"""Subject: {subject}\n\n{body}"""

        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        
        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")
        
        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")
        
        status_code, response = smtp.login(self.smtp_username, self.smtp_password)
        print(f"[*] Logging in: {status_code} {response}")
        
        smtp.sendmail(from_email, to_email, message)
        smtp.quit()

