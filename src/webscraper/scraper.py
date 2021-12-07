from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from api import Coursera


def get_cauth():
    with open("cauth_cookie.txt","r") as f:
        auth_cookie = f.read()

    return auth_cookie



def main():
    
    cauth = get_cauth()

    # specify the location to download the lecture data
    session = Coursera(cauth, "../../data")

    # specify the class to download
    session.download_class("cs-410")


if __name__ == '__main__':
    main()
