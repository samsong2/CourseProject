from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from api import Coursera


def get_cauth():
    with open("cauth_cookie.txt","r") as f:
        auth_cookie = f.read()

    return auth_cookie



def main():
    
    cauth = get_cauth()

    session = Coursera(cauth, "../../data")

    session.download_class("cs-410")


if __name__ == '__main__':
    main()
