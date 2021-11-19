from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from api import Coursera

from coursera_spider import CourseraSpider

def get_cauth():
    with open("cauth_cookie.txt","r") as f:
        auth_cookie = f.read()

    return auth_cookie



def main():
    
    cauth = get_cauth()

    session = Coursera(cauth, "../../data")

    session.download_class("cs-410")


# downloads 1 lecture
def test():

    cauth = get_cauth()

    session = Coursera(cauth, "../../data")

    session.download_lecture('https://www.coursera.org/learn/text-retrieval/lecture/rLpwp/lesson-1-1-natural-language-content-analysis')


if __name__ == '__main__':
    main()
