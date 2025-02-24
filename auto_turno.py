import os
import sys
import time
import imaplib
import email
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from smtp_notify import SMTPNotifier
from dotenv import load_dotenv

load_dotenv()

# Replace 'your_website_url' with the actual website URL you want to interact with
website_url = 'https://prenotami.esteri.it/Home?ReturnUrl=%2fServices'

# Set up the Chrome WebDriver (you can choose other browsers too)
driver = webdriver.Chrome()

# Replace 'your_email' with your actual email to receive notifications
from_email = 'auto-prenota@outlook.com'
to_email = os.environ['GMAIL_USERNAME']

IMAP_SERVER = "imap.gmail.com"  # Cambiar si usas otro proveedor
EMAIL_ACCOUNT = os.environ['PRENOTA_USERNAME']
EMAIL_PASSWORD = os.environ['GMAIL_PASSWORD']

notifier = SMTPNotifier("smtp-mail.outlook.com", 
                        587, 
                        "auto-prenota@outlook.com", 
                        "kiMtub-5gawco-hugqet")

def login_is_required():
    try:
        # Find the login button element
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/button'))
        )
        return True  # Element found, login is required
    except:
        return False  # Element not found, no login required

def perform_login():
    # Find the login form and input fields
    username_input = driver.find_element(By.XPATH, '//*[@id="login-email"]')
    password_input = driver.find_element(By.XPATH, '//*[@id="login-password"]')

    # Enter your username and password
    username_input.send_keys(os.environ['PRENOTA_USERNAME'])
    password_input.send_keys(os.environ['PRENOTA_PASSWORD'])

    # Submit the form
    login_button = driver.find_element(
        By.XPATH, '//*[@id="login-form"]/button')
    login_button.click()

def got_in():
    try:
        # If the OK Button appears it means there is no turn available
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button'))
        )
        return False  # Element found (no turn available)
    except:
        return True  # Element not found (turn available)
    
def go_to_services():
    # Find the book tab button element
    tab_button = driver.find_element(
        By.XPATH, '//*[@id="advanced"]')
    tab_button.click()
    time.sleep(1)
    
def check_PrivacyCheckBox():
    privacy_checkbox = driver.find_element(
        By.XPATH, '//*[@id="PrivacyCheck"]')
    privacy_checkbox.click()
    time.sleep(1)
        
def go_forward():
    # -- boton para avanzar
    forward_button = driver.find_element(
        By.XPATH, '//*[@id="btnAvanti"]')
    forward_button.click()
    time.sleep(1)
    
def fill_first_from():
    #-- reserva unica (no se toca)
    
    # -- input: nombre del progenitor del cual toma la ciudadania
    first_name = driver.find_element(
        By.XPATH, '//*[@id="DatiAddizionaliPrenotante_0___testo"]')
    first_name.send_keys(os.environ['PRENOTA_NOMBRE_COMPLETO'])
    time.sleep(1)
    
    # -- input: lugar de nacimiento del progenitor
    place_of_birth = driver.find_element(
        By.XPATH, '//*[@id="DatiAddizionaliPrenotante_1___testo"]')
    place_of_birth.send_keys(os.environ['PRENOTA_LUGAR_NACIMIENTO'])
    time.sleep(1)
    
    # -- input: fecha de nacimiento del progenitor (dd/mm/yyyy) (no hace falta poner / en el input)
    birth_date = driver.find_element(
        By.XPATH, '//*[@id="DatiAddizionaliPrenotante_2___data"]')
    birth_date.send_keys(os.environ['PRENOTA_FECHA_NACIMIENTO'])
    time.sleep(1)
    
    # -- input: direccion completa de residencia
    address = driver.find_element(
        By.XPATH, '//*[@id="DatiAddizionaliPrenotante_3___testo"]')
    address.send_keys(os.environ['PRENOTA_DIRECCION'])
    time.sleep(1)
    
    
def get_otp_code():
    # -- boton para enviar codigo al mail
    otp_button = driver.find_element(
        By.XPATH, '//*[@id="otp-send"]')
    otp_button.click()
    time.sleep(2)
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        # Buscar correos con el asunto "OTP Code"
        result, data = mail.search(None, '(SUBJECT "OTP Code")')
        email_ids = data[0].split()
        if not email_ids:
            print("No se encontraron correos con el asunto 'OTP Code'.")
            return None

        latest_email_id = email_ids[-1]  # Último correo recibido
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Obtener el cuerpo del correo
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode().strip()
                    break
        else:
            body = msg.get_payload(decode=True).decode().strip()

        # Extraer solo los números después de "OTP Code:"
        match = re.search(r"OTP Code:(\d{6})", body)  # Busca 6 dígitos después de "OTP Code:"
        if match:
            return match.group(1)  # Retorna solo los números
        else:
            print("No se encontró un código OTP en el correo.")
            return None
    except Exception as e:
        print("Error al obtener el código:", e)
        return None
    finally:
        mail.logout()
    
    
def fill_otp_code(code):
    # -- input: codigo de verificacion
    otp_code_input = driver.find_element(
        By.XPATH, '//*[@id="otp-input"]')
    otp_code_input.send_keys(code)
    time.sleep(1)



def fill_calendar():
    XPATH_TABLA = '//*[@id="datetimepicker"]/div/ul/ul/div/div[1]/table'
    XPATH_LUGAR_LIBRE = '//*[@id="datetimepicker"]/div/ul/ul/div/div[1]/table/tbody/tr/td[contains(@class, "free")]'  # Ajustar según la clase de los lugares libres
    XPATH_SIGUIENTE_MES = '//*[@id="datetimepicker"]/div/ul/ul/div/div[1]/table/thead/tr[1]/th[3]/span'
    XPATH_HORARIO = '//*[@id="loader-content"]/section[1]/div/div/div[2]/section/div[2]/ol/li[19]/div/div'
    
    for _ in range(12): # Intentar buscar fechas libres en los próximos 12 meses
        try:
            # Intentar encontrar un lugar libre
            lugares_libres = driver.find_elements(By.XPATH, XPATH_LUGAR_LIBRE)

            if lugares_libres:
                lugares_libres[0].click()  # Clic en el primer lugar libre disponible
                print("Fecha libre seleccionada.")
                time.sleep(2)  # Esperar a que cargue el horario
            
                # Seleccionar un horario disponible
                horario = driver.find_element(By.XPATH, XPATH_HORARIO)
                horario.click()
                print("Horario seleccionado.")
                return True  # Salir de la función porque ya encontró un espacio y horario

            # Si no hay lugares libres, pasar al siguiente mes
            print("No hay fechas libres este mes, pasando al siguiente...")
            next_month = driver.find_element(By.XPATH, XPATH_SIGUIENTE_MES)
            next_month.click()
            time.sleep(2)  # Esperar a que cargue el nuevo mes

        except Exception as e:
            print(f"Error al buscar fecha libre: {e}")

    print("No se encontraron fechas libres en los próximos meses.")
    return False  # No encontró ninguna fecha libre
        
        
def make_appointment():
    fill_first_from()
    code = get_otp_code()
    fill_otp_code(code)
    check_PrivacyCheckBox()
    go_forward()
    fill_calendar()
    # prenota()

def main(book_type):
    # Open the website
    driver.get(website_url)

    try:
        if login_is_required():
            perform_login()
        
        # Make an appoinment
        book_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="dataTableServices"]/tbody/tr[{book_type}]/td[4]/a/button'))
        )
        book_button.click()
        
        if got_in():
            make_appointment()
            # notifier.send_email(from_email, to_email, 
            #                     'Conseguiste turno!', 
            #                     'Conseguiste entrar a la pagina para sacar el turno! \nEntra a https://prenotami.esteri.it/Home?ReturnUrl=%2fServices para saber como seguir. \n \n Saludos, \n Prenota Bot')
            # check_PrivacyCheckBox()
            # go_forward()
        else:
            # Close the browser
            driver.quit()
            notifier.send_email(from_email, to_email, 
                                'Turno no disponible', 
                                'Lamento informarte que actualmente no hay turnos disponibles. Seguiremos probando hasta conseguirlo. Gracias por tu paciencia.')

    except Exception as e:
        print("An error occurred:", str(e))
        

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        main('2')
        

# //*[@id="typeofbookingddl"]
# //*[@id="DatiAddizionaliPrenotante_0___testo"]
# //*[@id="DatiAddizionaliPrenotante_1___testo"]
# //*[@id="DatiAddizionaliPrenotante_2___data"]
# //*[@id="DatiAddizionaliPrenotante_3___testo"]
# # notas
# //*[@id="BookingNotes"]
# # codigo
# //*[@id="otp-input"]
# # boton codigo
# //*[@id="otp-send"]
# # boton siguiente
# //*[@id="btnAvanti"]
# # seleccionar terminos y privacidad
# //*[@id="PrivacyCheck"]
# # boton avance
# //*[@id="btnAvanti"]

