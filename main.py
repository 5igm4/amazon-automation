#coding: utf-8

import time
import buysol

from logger import l
from selenium import webdriver


def run_workflow(b):
    # Waits until item is in stock and adds to cart

    buysol.check_item_stock(b)
    buysol.add_to_cart(b)
    buysol.print_subtotal(b)

# ITEM_URL = 'https://www.amazon.com/Accoutrements-11761-Yodelling-Pickle/dp/B0010VS078/ref=sr_1_1'


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    try:
        l('Starting Chromium')
        b = webdriver.Chrome('./chromedriver', options=options)
        b.implicitly_wait(2)
        l('Succesfully started Chromium')
    except Exception as e:
        l('Failed to open browser: {}'.format(e))
        exit()

    try:
        buysol.login(b)
    except Exception as e:
        l('Error Could not login: {}'.format(e))
        exit(1)

    try:
        done = False
        while(not done):
            try:
                run_workflow(b)
                done = True
            except KeyboardInterrupt:
                done = True
            except BaseException:
                pass
    except Exception as e:
        l('ERROR: {}'.format(e))
    finally:
        l('Closing Chromium')
        try:
            b.close()
        except BaseException:
            pass
        l('Closed Chromium')

    l('ALL DONE')

    # p = b.find_element_by_css_selector('td.grand-total-price').text
    # if int(p.split(' ')[1].replace(',', '')) > LIMIT_VALUE:
    #     l('PLICE IS TOO LARGE.')
    #     continue

    # b.find_element_by_name('placeYourOrder1').click()
    # break
