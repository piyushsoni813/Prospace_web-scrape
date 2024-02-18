POSTGRES_DB = 'Test'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'your_password'
POSTGRES_HOST = 'your_database_host'
POSTGRES_PORT = 'your_database_port'

ITEM_PIPELINES = {
    'your_project_name.pipelines.PostgresPipeline': 300,
}



# import web driver
from selenium import webdriver

# create ChromeOptions object
chrome_options = webdriver.ChromeOptions()

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(options=chrome_options)

# driver.get method() will navigate to a page given by the URL address
driver.get('http://www.linkedin.com')
