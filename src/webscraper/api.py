from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

# improve sait response?
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import json
import os
from pathlib import Path

from collections import deque

from urllib import parse

import re

# current trime 12 minutes to download

class Coursera:

    def __init__(self, cauth, download_path = "."):

        options = Options()
        options.headless = True
        options.add_argument('--log-level=2')
        options.add_argument("--disable-extensions"); # disabling extensions
        #options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
        #options.add_argument("--no-sandbox"); # Bypass OS security model

        self.auth_cookie = {"name": "CAUTH", "value": cauth}
        # for webcrawling
        self.domain = "https://www.coursera.org"
        
        self.driver = webdriver.Chrome('./chromedriver',options=options)
        self.driver.get(self.domain)
        self.driver.add_cookie(self.auth_cookie)

        # set download path
        self.download_directory = download_path
        self.download_path = self.download_directory

    def __del__(self):
        self.driver.quit()
        
    # downloads all the lectures for a class
    def download_class(self, class_name):
        # need to navigate to welcome page? 

        class_home_page= f'https://www.coursera.org/learn/{class_name}/home/welcome'

        # check for rc-WeekCollectionNavigationItem to get weeks?
        
        home_soup = self.get_html_soup(class_home_page, 5)

        weeks = self.parse_home_page(home_soup)
        
        if len(weeks) > 0:
            try:
                self.download_path = os.path.join(self.download_directory, class_name)
                os.makedirs(self.download_path, exist_ok=True)

                for week in weeks:
                    #print(week_url)
                    self.download_week(week)
                    # for each week get lecture 
                        # for each lecture parse

            except FileExistsError:
                print("Directory for {} already exists".format(class_name))
            # directory already exists
        else:
            print("Error: Unable to find lectures for this class")
            return
        

    def download_week(self, week_url):
        week_soup = self.get_html_soup(week_url, 5)

        lectures = self.parse_week_page(week_soup)

        for lecture in lectures:
            print(lecture)
            self.download_lecture(lecture)


    # downloads a lecture given its class na
    #def download_lecture(self, url)
    def download_lecture(self, lecture_url):
    
        # construct lecture url
        url = parse.urlparse(lecture_url)

        class_name = ""
        lecture_name = ""

        if re.match("\/learn\/.+\/lecture\/.+", url.path):
            url_path_directory = url.path.strip('/').split('/')
            class_name = url_path_directory[1]
            lecture_name = url_path_directory[-1]
        else:
            print("Invalid lecture URL")
            return

        soup = self.get_html_soup(lecture_url, 5)

        video_link, lecture_timestamp, lecture_data = self.parse_lecture(soup)
        
        download_path = os.path.join(self.download_path, lecture_name + ".txt")
        # write downloaded to file
        with open(download_path,"w") as f:
            # video_link at the start of file?
            f.write(lecture_name + '\n')
            f.write(video_link + '\n')
            for j in range(len(lecture_data)):
                f.write(lecture_timestamp[j] + " : " + lecture_data[j] + "\n")

    
    def get_html_soup(self, url, delay = 1):
        self.driver.get(url)

        time.sleep(delay)

        """
        try:
            rendered = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME , 'a')))
            for l in rendered:
               self.handle_link(l.get_attribute('href'))

        except Exception as e:
            print("Failed {} to load in time".format(url))
        """

        res_html = self.driver.execute_script('return document.body.innerHTML')

        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content

        return soup


            
    # given a link pass it to other function
    # unused function
    def handle_link(self, link):

        some_url = parse.urlparse(link)
        # insite move
        if some_url.netloc == "":
            some_url = some_url._replace(scheme="https", netloc="www.coursera.org")
        
        path = some_url.path
        if re.match("\/learn\/.+\/lecture\/.+", path):
            # download lecture
            print("Lecture", some_url)
                
        elif re.match("\/learn\/.+\/home\/.+", path):
            # searchable page for more links
            print("Home page", some_url)
                


    # look for links to the weeks
    def parse_home_page(self, soup):
        nav_weeks = soup.find_all('a', {"data-click-key" : "open_course_home.menu.click.nav_week"})

        weeks_url = []

        for w in nav_weeks:
            url = parse.urljoin("https://www.coursera.org", w.get('href'))
            weeks_url.append(url)

        return weeks_url


    # look for links to the lecture in each week
    def parse_week_page(self, soup):
        
        links = soup.find_all('a', {'data-click-key' : 'open_course_home.period_page.click.item_link'})

        lecture_urls = []
        for l in links:
            # filter for lectures
            path = l.get('href')
            if re.match("\/learn\/.+\/lecture\/.+", path):
                url = parse.urljoin("https://www.coursera.org", path)
                lecture_urls.append(url)

        return lecture_urls

    # parses lecture webpage for information
    def parse_lecture(self, soup):
        
        video_link = soup.find('video').get("src")

        timestamps = soup.find_all('button',{"class" : "timestamp"})
        data = soup.find_all('div', {"class" : "phrases"})

        text_timestamp = [t.contents[1] for t in timestamps]
        text_data = [d.text for d in data]

        return video_link, text_timestamp, text_data
