import os
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
        # Find the OK button element
        driver.find_element(
            By.XPATH, '//html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button')
        return True  # Element found
    except:
        return False  # Element not found

def main():
    # Open the website
    driver.get(website_url)

    try:
        if login_is_required():
            perform_login()
        
        # Make an appoinment
        element_to_click = driver.find_element(
            By.XPATH, '//*[@id="dataTableServices"]/tbody/tr[1]/td[4]/a/button')
        element_to_click.click()

        # Wait for a while to see the changes
        time.sleep(5)
        
        if got_in():
            notifier.send_email(from_email, to_email, subject, body)
        else:
            # Close the browser
            driver.quit()

    except Exception as e:
        print("An error occurred:", str(e))
        

if __name__ == "__main__":
    main()