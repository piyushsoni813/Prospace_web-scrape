from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

class WebConnector:
    def __init__(self):
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = webdriver.ChromeOptions()
        return webdriver.Chrome(options=chrome_options)

    def wait_for_element(self, by, value, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            print(f"Timeout waiting for element {by}: {value}")
            return None

    def close_driver(self):
        self.driver.quit()

    def login(self):
        self.driver.get('http://www.linkedin.com')

        
        load_dotenv()
        linkedin_password = os.getenv('linkedin_pw')
        linkedin_username = os.getenv('linkedin_uid')

        # Login logic
        email_input = self.wait_for_element(By.ID, 'session_key')
        email_input.send_keys(linkedin_username)

        password_input = self.wait_for_element(By.ID, 'session_password')
        password_input.send_keys(linkedin_password)

        log_in_button = self.wait_for_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width')
        log_in_button.click()

# Create a single instance of WebConnector
linkedin_scraper = WebConnector()
linkedin_scraper.login()