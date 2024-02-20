import os
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import psycopg2

class webconnector:
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


if __name__ == "__main__":
    linkedin_scraper = webconnector()

    linkedin_scraper.driver.get('http://www.linkedin.com')

    load_dotenv()
    linkedin_password = os.getenv('linkedin_pw')
    linkedin_username = os.getenv('linkedin_uid')

    # Login logic
    email_input = linkedin_scraper.wait_for_element(By.ID, 'session_key')
    email_input.send_keys(linkedin_username)

    password_input = linkedin_scraper.wait_for_element(By.ID, 'session_password')
    password_input.send_keys(linkedin_password)

    log_in_button = linkedin_scraper.wait_for_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width')
    log_in_button.click()

    # Search logic
    search_button = linkedin_scraper.wait_for_element(By.CLASS_NAME, 'search-global-typeahead__collapsed-search-button')
    search_button.click()

    search_input = linkedin_scraper.wait_for_element(By.CLASS_NAME, 'search-global-typeahead__input')
    search_input.clear()
    search_input.send_keys('Software Developer')
    search_input.send_keys(Keys.RETURN)

    button = linkedin_scraper.wait_for_element(By.XPATH, '//button[text()="People"]')
    button.click()

    total_pages = 1  # Set the desired number of pages
    page_count = 0

    profile_links = []
    for page in range(total_pages):
        # Wait for search results to load
        search_link = "https://www.linkedin.com/search/results/people/?keywords=software%20developer&origin=SWITCH_SEARCH_VERTICAL&page=" + str(page_count + 1)
        search_results = linkedin_scraper.driver.get(search_link)
        search_results = linkedin_scraper.wait_for_element(By.XPATH, '//li[@class="reusable-search__result-container"]')

        # Your existing logic to retrieve profile links
        html_page = linkedin_scraper.driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        span_tags = soup.find_all('span', class_='entity-result__title-text t-16')

        for span_tag in span_tags:
            app_aware_links = span_tag.find_all('a', class_='app-aware-link')
            href_links = [link.get('href') for link in app_aware_links]
            for href_link in href_links:
                profile_links.append(href_link)
        page_count += 1
        sleep(1)
    
    for person_link in profile_links:
        person_page = linkedin_scraper.driver.get(person_link)
        html_page = linkedin_scraper.driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')

        name = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text
        position = soup.find('div', class_='text-body-medium break-words').text
        skill_link = soup.find('a', class_="optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid").get('href')
        
        print("Name:", name, "Position:", position, "Skill_Link:", skill_link)

        
