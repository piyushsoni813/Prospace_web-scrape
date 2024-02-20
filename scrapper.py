import psycopg2
from psycopg2 import Error
import os
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from webdriver import linkedin_scraper

if __name__ == "__main__":
    while True:
        user_interrupt = input("Press Enter to proceed: ")
        if not user_interrupt:  # Check if the input is empty
            break

    search_button = linkedin_scraper.wait_for_element(By.CLASS_NAME, 'search-global-typeahead__collapsed-search-button')
    search_button.click()

    search_input = linkedin_scraper.wait_for_element(By.CLASS_NAME, 'search-global-typeahead__input')
    search_input.clear()
    search_input.send_keys('Software Developer')
    search_input.send_keys(Keys.RETURN)

    button_people = linkedin_scraper.wait_for_element(By.XPATH, '//button[text()="People"]')
    button_people.click()

    total_pages = 35  # Set the desired number of pages
    page_count = 0

    csv_file_path = 'output.csv'

    # Establishing a connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('db_name'),
            user=os.getenv('db_user'),
            password=os.getenv('db_password'),
            host=os.getenv('db_host'),
            port=os.getenv('db_port')
        )
        cur = conn.cursor()

        # Check if the table exists, if not, create it
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Prospace_algobulls (
                name VARCHAR,
                position VARCHAR,
                person_link VARCHAR,
                skills VARCHAR
            )
        """)
        conn.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    profile_links = []
    for page in range(total_pages):
        # Wait for search results to load
        search_link = "https://www.linkedin.com/search/results/people/?keywords=software%20developer&origin=SWITCH_SEARCH_VERTICAL&page=" + str(page_count + 1)
        search_results = linkedin_scraper.driver.get(search_link)
        linkedin_scraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.1)
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
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['name', 'position', 'person_link', 'skills'])
        
        for person_link in profile_links:
            sleep(2)
            linkedin_scraper.driver.get(person_link)
            linkedin_scraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.1)
            person_html_page = linkedin_scraper.driver.page_source
            soup = BeautifulSoup(person_html_page, 'html.parser')
            name = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text.strip()
            position = soup.find('div', class_='text-body-medium break-words').text.strip()
            sleep(1)
            
            try:
                section_element = linkedin_scraper.driver.find_element('xpath',"//section[div[@id='skills']]")
                anchor_tag = section_element.find_elements('xpath' , ".//a")
                skill_link = anchor_tag[-1].get_attribute("href")
                linkedin_scraper.driver.get(skill_link)
                sleep(0.5)
                linkedin_scraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(0.1)
                skills_html_page = linkedin_scraper.driver.page_source
                soup = BeautifulSoup(skills_html_page, 'html.parser')
                skill_span_elements = soup.find_all('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
                skill_span_html_code = ""
                for element in skill_span_elements:
                    skill_span_html_code += str(element)
                skill_soup = BeautifulSoup(skill_span_html_code, 'html.parser')
                span_elements = skill_soup.find_all('span', {'aria-hidden': 'true'})
                skill_list = [span.get_text(strip=True) for span in span_elements]
                skills = ''
                skills = "|".join(skill_list)
                print(skills)
            except:
                skills = "NOT PRESENT"
            print("Name: ", name, " Position: ", position, " UserLink: ", person_link, " Skill-Set: ", skills)
            writer.writerow([name, position, person_link, skills])
            sql = "INSERT INTO Prospace_algobulls (name, position, person_link, skills) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (name, position, person_link, skills))
            conn.commit()
        
    print("CSV file saved successfully.")
    print("Data Saved Succesfully in SQL Server")
    linkedin_scraper.close_driver()
    cur.close()
    conn.close()
