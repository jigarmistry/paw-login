import sys
import time
import platform
import configparser
from selenium import webdriver

phantom_path = "/usr/local/lib/phantomjs/bin/phantomjs"

if platform.system() == "Darwin":
    phantom_path = "/usr/local/bin/phantomjs"

browser = webdriver.PhantomJS(
    phantom_path,
    service_args=[
        '--ssl-protocol=any', '--ignore-ssl-errors=true', '--load-images=no'
    ])

browser.set_window_size(1400,1000)

url_paw = "https://www.pythonanywhere.com/login/"


def get_credentials():
    file_name = "crds.ini"

    config = configparser.ConfigParser()
    config.read(file_name)
    sites = config.sections()
    dictCreds = {}

    if len(sites) == 0:
        return dictCreds, False

    for site in sites:
        dictCreds[site] = {}
        dictCreds[site]["username"] = config[site]["username"]
        dictCreds[site]["password"] = config[site]["password"]
    return dictCreds, True


def do_login(site, data):

    try:
        browser.get(url_paw)
        userNameElem = browser.find_element_by_id('id_auth-username')
        userNameElem.send_keys(data["username"])
        passwordElem = browser.find_element_by_id('id_auth-password')
        passwordElem.send_keys(data["password"])
        logInBtnElem = browser.find_element_by_id('id_next')
        logInBtnElem.click()
        try:
            # browser.get_screenshot_as_file("rr.png")
            webLinkElem = browser.find_element_by_id('id_web_app_link')            
            webLinkElem.click()            
            appExtendElem = browser.find_element_by_css_selector(
                '.btn.btn-warning.webapp_extend')            
            appExtendElem.click()
            expiryNoteElem = browser.find_element_by_class_name(
                'webapp_expiry')            
            print(site + " : " + expiryNoteElem.text)
        except Exception as e:
            print("Credentials are wrong for " + site)
            print("Exception : " + str(e))
    except Exception as e:
        print("Something went wrong for " + site)
        print("Exception : " + str(e))


if __name__ == "__main__":
    creds, st = get_credentials()
    if st:
        for site, value in creds.items():
            do_login(site, value)
    else:
        print("No Credentials Data Found")
