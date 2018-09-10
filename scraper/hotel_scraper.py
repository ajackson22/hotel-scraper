import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


dateFormat = "%m/%d/%Y"

def render_page(url):
    # chrome_options = Options()
    # chrome_options.add_argument("--window-size=1920,1080");
    # chrome_options.add_argument("--disable-gpu");
    # chrome_options.add_argument("--disable-extensions");
    # chrome_options.add_argument("--proxy-server='direct://'");
    # chrome_options.add_argument("--proxy-bypass-list=*");
    # chrome_options.add_argument("--start-maximized");
    # chrome_options.add_argument("--headless");

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    # driver.quit()
    return r

def parse_date(date):
    d = datetime.datetime.strptime(date, dateFormat)
    return d



def find_availability(checkin, checkout, location):
    # checkin = parse_date(ci)
    # checkout = parse_date(co)
    availability = {}

    checkinMonth = checkin.month - 1
    checkinDay = checkin.day
    checkinYear = checkin.year
    checkoutMonth = checkout.month - 1
    checkoutDay = checkout.day
    checkoutYear = checkout.year

    url_val = 'https://www.ihg.com/hotels/us/en/find-hotels/hotel/list?' \
              'qDest='+location+'&' \
              'qCiMy='+str(checkinMonth)+str(checkinYear)+'&' \
              'qCiD='+str(checkinDay)+'&' \
              'qCoMy='+str(checkoutMonth)+str(checkoutYear)+'&' \
              'qCoD='+str(checkoutDay)+'&' \
              'qAdlt=1&' \
              'qChld=0&' \
              'qRms=1&' \
              'qRtP=6CBARC.IVANI'

    print("Finding availability for" + location + ": " + str(checkin) + " -> " + str(checkout))

    r = render_page(url_val)

    soup = BeautifulSoup(r, "html.parser")
    hotels = soup.findAll("div", {"id": re.compile('hotelId-*')})
    for h in hotels:
        isAvailable = False
        hotelNames = h.findChildren("span", {"data-slnm-ihg": re.compile('hotelName')})
        for hn in hotelNames:
            hotelName = hn.a.text

        hotelPoints = h.findChildren("div", {"class": re.compile('pncPointsContainer')})
        for hp in hotelPoints:
            hotelPoint = hp.span.text
            isAvailable = True;

        if (isAvailable == False) :
            availability[hotelName] = "Not Availabile"
        else:
            availability[hotelName] = hotelPoint

    return availability