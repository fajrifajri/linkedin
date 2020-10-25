from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
from pymongo import MongoClient
from credential import *


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

keywords = ["site reliability engineer","technical marketing engineer","5G","software engineer","network engineer","qa engineer"]
locations = ["San Francisco Bay Area", "California, United States", "Texas, United States","Washington,, United States","Massachusetts, United States"]

linkedin_login_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
linkedin_job_url = "https://www.linkedin.com/jobs/search/?"

### Database Connection
client = MongoClient('172.18.0.1:27017',
                      username='jobs',
                      password='jobs',
                      authSource='jobs',
                      authMechanism='SCRAM-SHA-1')

db = client["jobs"]
jobs = db["jobs"]

class linkedin(object):
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_process(self):
        # driver.get method() will navigate to a page given by the URL address
        self.driver.get(linkedin_login_url)

        # enter username
        username = self.driver.find_element_by_id('username')
        username.clear()
        username.send_keys(user)
        time.sleep(0.5)

        # enter password
        password = self.driver.find_element_by_id('password')
        password.clear()
        password.send_keys(passwd)
        time.sleep(0.5)

        # login by class name
        self.driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        time.sleep(0.5)

    def jobs(self, key, loc):
        key = key.replace(" ", "%20")
        loc = loc.replace(" ", "%20").replace(",","%2C")
        url = linkedin_job_url + "&keywords=" + key + "&location=" + loc
        self.driver.get(url)
        result = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(result, "html.parser").findAll("small", {"class": "display-flex t-12 t-black--light t-normal"})
        for res in soup:
            num = res.text.strip().split(" ")[0]
        return(int(num.replace(',', '')))


    def close_browser(self):
        self.driver.close()
        self.driver.quit()

def insert_db(key,loc, total):
    data_query = {"keyword":key,"loc":loc}
    data_result = jobs.find(data_query)
    a = 0
    for index, item in enumerate(data_result):
        a += 1
    
    # update if data exists
    if(a==1):
        data_update = { "$set": { 'total': total } } 
        jobs.update_one(data_query, data_update)
    
    # insert if data not exists
    else:
        data = {"keyword":key,"loc":loc,"total":total}
        jobs.insert_one(data)

if __name__ == "__main__":
    jobs_data = linkedin()
    jobs_data.login_process()
    for key in keywords:
        for loc in locations:
            time.sleep(random.randint(1, 5))
            insert_db(key, loc, jobs_data.jobs(key,loc))

    jobs_data.close_browser()