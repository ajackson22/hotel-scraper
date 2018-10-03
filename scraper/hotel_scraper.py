from bs4 import BeautifulSoup
import time
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    # driver.quit()
    return driver

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

    url_val = "https://www.ihg.com/hotels/us/en/find-hotels/hotel/list?qDest=Bora%20Bora,%20French%20Polynesia&qCiMy=92018&qCiD=27&qCoMy=92018&qCoD=28&qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC.IVANI&qAkamaiCC=US&qSrt=sDD&qBrs=ic.in.vn.cp.hi.ex.rs.cv.sb.cw.ma.ul.ki.va&qAAR=6CBARC.IVANI&srb_u=1&qRad=50&qRdU=km"

    print("Finding availability for" + location + ": " + str(checkin) + " -> " + str(checkout))

    driver = render_page(url_val)
    r = driver.page_source

    soup = BeautifulSoup(r, "html.parser")

    not_available_link = driver.find_elements_by_link_text("View available dates")

    if (not_available_link):
        for link in not_available_link:
            # Open Calendar for hotel
            link.click()

            month_element_class = "ihgcal-monthTitleText"
            month = driver.find_element_by_xpath("//span[contains(@class, '" + month_element_class +"')]")

            avail_dates_btn = driver.find_elements_by_css_selector(".dp-btn.dp-btn-default.dp-btn-sm")

            for btn in avail_dates_btn:
                day_div = btn.find_element_by_class_name("ng-binding")
                print(day_div)
                day = day_div.text
                print(day)



            # Close Calendar for hotel
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "calCloseIcon")))
            element.click()


    # hotels = soup.findAll("div", {"id": re.compile('hotelId-*')})
    # for h in hotels:
    #     isAvailable = False
    #     hotelNames = h.findChildren("span", {"data-slnm-ihg": re.compile('hotelName')})
    #     for hn in hotelNames:
    #         hotelName = hn.a.text
    #
    #     hotelPoints = h.findChildren("div", {"class": re.compile('pncPointsContainer')})
    #     for hp in hotelPoints:
    #         hotelPoint = hp.span.text
    #         isAvailable = True;
    #
    #     if (isAvailable == False) :
    #         availability[hotelName] = "Not Availabile"
    #     else:
    #         availability[hotelName] = hotelPoint

    return availability