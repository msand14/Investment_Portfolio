import time
import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# from modules.loadingConfigurations import *
# from modules.loggingSettings import *
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


PATH = "C:\Program Files (x86)\chromedriver.exe"

Scrapping_config = {'User-Agent': 'Mozilla/5.0 (' +
                                  'Macintosh; Intel Mac OS X 10_11_5)' +
                                  ' AppleWebKit/537.36' +
                                  '(KHTML, like Gecko) ' +
                                  'Chrome/50.0.2661.102 Safari/537.36'}


def getSoup(link, headers: dict):
    """
    Gets the Soup for scrapping
    :param link: URL where the information is located on the Internet
    :param headers: Useful for the permission settings
    :return: The BeautifulSoup object represents the parsed document as a whole.
    """
    time.sleep(3)
    page = requests.get(link, headers=headers)
    if page.status_code != 200:
        logging.error('ERROR ' + getSoup.__name__ + ': Error de conexión')
        logging.error(link)
        logging.error(str(page))
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def initSoup(url):
    """
    Initialise all the procedure to scrap the Data
    :param url: string, Web URL to scrap the historical data
    :return: Beautiful Soup
    """
    soup = getSoup(link=url, headers=Scrapping_config)
    return soup


def initDriver(URL='https://es.investing.com/funds/IE00BD0NCM55'):
    driv = webdriver.Chrome(ChromeDriverManager().install())
    URL = URL.lower()
    options = Options()
    options.add_argument('--disable-logging')
    # driv = webdriver.Chrome(executable_path=PATH)
    driv.get(URL)
    driv.maximize_window()
    return driv

def getHistorical(ticker: str, fromDate='01/01/2019', Mode='fund'):
    """
    Get the Historical weekly Prices from a ticker
    :param ticker: ISIN from a fund
    :return: Pandas DataFrame containing the Date and the Prices
    """

    logging.info('Releasing the Spider')

    ticker_low = ticker.lower()
    if Mode.lower() == 'fund':
        basic_investing_url = 'https://es.investing.com/funds/'
    else:
        basic_investing_url = 'https://es.investing.com/etfs/'
    historical_data_investing_low = (basic_investing_url + ticker_low +
                                     '-historical-data')
    historical_data_investing_upp = (basic_investing_url + ticker +
                                     '-historical-data')

    result_status = requests.get(url=historical_data_investing_low,
                                 headers=Scrapping_config).status_code
    if result_status != 403 and result_status != 404:
        driver = initDriver(URL=historical_data_investing_low)
    else:
        driver = initDriver(URL=historical_data_investing_upp)
    time.sleep(5)
    try:
        driver.find_element_by_id('onetrust-accept-btn-handler').click()
    except:
        logging.debug('First pop up doesnt appear')
    time.sleep(1)
    try:
        driver.find_element_by_class_name('largeBannerCloser').click()
    except:
        logging.debug('largebanner doesnt appear')

    try:
        driver.find_elements_by_id('flatDatePickerCanvasHol')[0].click()
    except:
        driver.find_element_by_class_name('largeBannerCloser').click()
        driver.find_elements_by_id('flatDatePickerCanvasHol')[0].click()

    driver.find_element_by_id('startDate').clear()

    driver.find_element_by_id('startDate').send_keys(fromDate)
    time.sleep(1)
    try:
        driver.find_element_by_id('applyBtn').click()
    except:
        driver.find_element_by_class_name('largeBannerCloser').click()
        time.sleep(1)
        driver.find_element_by_id('applyBtn').click()
    try:
        interval = Select(driver.find_element_by_id("data_interval"))
        time.sleep(1)
        interval.select_by_value("Weekly")
        time.sleep(2)
    except:
        driver.find_element_by_class_name('largeBannerCloser').click()
        interval = Select(driver.find_element_by_id("data_interval"))
        interval.select_by_value("Weekly")
    name_active = driver.find_element_by_tag_name('h1').text
    name_active = (re.sub('\\(.+?\\)', '', name_active,
                          flags=re.DOTALL)).strip()
    time.sleep(2)
    try:
        hist_table = driver.find_element_by_id('curr_table').find_element_by_tag_name("tbody")
    except:
        try:
            driver.find_element_by_class_name('largeBannerCloser').click()
            hist_table = driver.find_element_by_id('curr_table').find_element_by_tag_name("tbody")
        except:
            hist_table = driver.find_element_by_id('curr_table').find_element_by_tag_name("tbody")

    dates = []
    prices = []
    trs = hist_table.find_elements_by_tag_name("tr")
    for tr in trs:
        tds = tr.find_elements_by_tag_name("td")
        dates.append(tds[0].text)
        prices.append(tds[1].text)

    data = {'Date': dates, 'Price': prices}
    df = pd.DataFrame(data=data)
    driver.close()
    return df, name_active