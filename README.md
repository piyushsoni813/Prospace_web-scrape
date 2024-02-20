# LinkedIn Scraper README

## Overview

This set of scripts is designed to scrape data from LinkedIn, specifically focusing on profiles related to the search term "Software Developer." The data extracted includes information such as name, position, profile link, and a list of skills. The scripts use Selenium for web scraping, Beautiful Soup for HTML parsing, and PostgreSQL for data storage.

## Prerequisites

1. **Python Environment:** Ensure you have Python installed on your system (preferably Python 3.x).

2. **Dependencies:** Install the required Python packages by running:

```bash
pip install psycopg2 selenium beautifulsoup4 python-dotenv
```

3. **WebDriver:** These scripts use the Chrome WebDriver. Make sure to download the appropriate version from [ChromeDriver](https://sites.google.com/chromium.org/driver/) and place it in your system's PATH.

4. Create a Python virtual environment {Python Version 3.10.11}
```bash
python -m venv your_venv_name
```
5. install PIP requirements from req.txt
for linux
```bash
source your_venv_name\bin\activate
pip install -r req.txt
```
for windows
```bash
./your_venv_name/Scripts/activate
pip install -r req.txt
```
## Configuration

1. **Environment Variables:** Create a `.env` file in the same directory as the scripts with the following content:

```env
  db_name=<your_database_name>
  db_user=<your_database_user>
  db_password=<your_database_password>
  db_host=<your_database_host>
  db_port=<your_database_port>
  linkedin_pw=<your_linkedin_password>
  linkedin_uid=<your_linkedin_username>
```

  Replace `<your_...>` with your actual database and LinkedIn credentials.

2. **Total Pages:** Adjust the `total_pages` variable in `script1.py` to control the number of pages to scrape.

## Running the Scripts

1. **Execute scrapper.py:** Open a terminal and run the following command:

```bash
  python scrapper.py
```

   The script will prompt you to press Enter to proceed. After completion, it will save the scraped data in both a CSV file (`output.csv`) and a PostgreSQL database.

2. **Execute webdriver.py:** There's no need to run this script separately. It is imported as a module in `scrapper.py` and used for initializing the WebDriver and logging into LinkedIn.

## Important Notes

- Ensure that you comply with LinkedIn's [robots.txt](https://www.linkedin.com/robots.txt) and [terms of service](https://www.linkedin.com/legal/user-agreement) to avoid any legal issues.

- The provided scripts are for educational purposes and may need adjustments based on changes to LinkedIn's website structure or terms of service.

## Disclaimer

The authors of these scripts are not responsible for any misuse or violation of terms and conditions on external websites. Use at your own discretion and responsibility.
