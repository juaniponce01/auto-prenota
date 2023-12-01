import smtplib
import getpass
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER=os.environ['SMTP_SERVER']
SMTP_PORT=os.environ['SMTP_PORT']
SMTP_USERNAME=os.environ['SMTP_USERNAME']
SMTP_PASSWORD=os.environ['SMTP_PASSWORD']

from_email = 'auto-prenota@outlook.com'
to_email = 'juaniponce0@gmail.com'
subject = 'Turno Conseguido!'
body = 'Conseguiste entrar a la pagina para sacar el turno! \nEntra a https://prenotami.esteri.it/Home?ReturnUrl=%2fServices para saber como seguir. \n \n Saludos, \n Prenota Bot'
message = f"Subject: {subject}\n\n{body}"
# message = """Subject: Turno Conseguido!

# Si te llego este mail, significa que consguiste un turno, felicidades! :D"""

smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
status_code, response = smtp.ehlo()
print(f"[*] Echoing the server: {status_code} {response}")
status_code, response = smtp.starttls()
print(f"[*] Starting TLS connection: {status_code} {response}")
status_code, response = smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
print(f"[*] Logging in: {status_code} {response}")
smtp.sendmail(from_email, to_email, message)
smtp.quit()