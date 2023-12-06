import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from smtp_notify import SMTPNotifier
from dotenv import load_dotenv

load_dotenv()

# Replace 'your_website_url' with the actual website URL you want to interact with
website_url = 'https://prenotami.esteri.it/Home?ReturnUrl=%2fServices'

# Set up the Chrome WebDriver (you can choose other browsers too)
driver = webdriver.Chrome()

# Replace 'your_email' with your actual email to receive notifications
from_email = 'auto-prenota@outlook.com'
to_email = 'juaniponce0@gmail.com'
subject = 'Turno Conseguido!'
body = 'Conseguiste entrar a la pagina para sacar el turno! \nEntra a https://prenotami.esteri.it/Home?ReturnUrl=%2fServices para saber como seguir. \n \n Saludos, \n Prenota Bot'

notifier = SMTPNotifier(os.environ['SMTP_SERVER'], 
                        os.environ['SMTP_PORT'], 
                        os.environ['SMTP_USERNAME'], 
                        os.environ['SMTP_PASSWORD'])

def login_is_required():
    try:
        # Find the login button element
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button')
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
    
    # Wait for a while to see the changes
    time.sleep(5)

def got_in():
    try:
        # If the OK Button appears it means there is no turn available
        driver.find_element(
            By.XPATH, '//html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button')
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
    forward_button = driver.find_element(
        By.XPATH, '//*[@id="btnAvanti"]')
    forward_button.click()
    time.sleep(1)

def main(book_type):
    # Open the website
    driver.get(website_url)

    try:
        if login_is_required():
            perform_login()
        
        # Make an appoinment
        book_reconstruction_button = driver.find_element(
            By.XPATH, '//*[@id="dataTableServices"]/tbody/tr[' + book_type + ']/td[4]/a/button')
        book_reconstruction_button.click()

        # Wait for a while to see the changes
        time.sleep(5)
        
        if got_in():
            notifier.send_email(from_email, to_email, 
                                'Conseguiste turno!', 
                                'Conseguiste entrar a la pagina para sacar el turno! \nEntra a https://prenotami.esteri.it/Home?ReturnUrl=%2fServices para saber como seguir. \n \n Saludos, \n Prenota Bot')
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
        
        