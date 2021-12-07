# WebScraper

The webscraper will, given a Coursera class name, attempt to download all lecture transcripts
and video links for that class.

This webscraper will only work for classes that you are/have been enrolled in.

## Instructions

### 1. install Selenium and Beautiful Soup  
'''python

'''


### 2. Download Chromedriver
Download the chromedriver for your version of Chrome.
Then put it in the webscraper directory.

You can go to 

### 3. Get CAUTH cookie value
To get your CAUTH cookie login to coursera.org.
Then go to chrome://settings/cookies/detail?site=coursera.org 
and copy the value of CAUTH into cauth_cookie.txt

### 4. Specify class and download location

### 5. Download the class
Now finally to scrape for all of the class lectures
'python scraper.py'   
