from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)

page = driver.get("https://www.google.com/")