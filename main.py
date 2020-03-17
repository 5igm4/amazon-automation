#coding: utf-8

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_ID = os.environ.get('UUID', None)
LOGIN_PASSWORD = os.environ.get('PASS', None)

HOME = 'https://www.amazon.com/'
ITEM_URL = 'https://www.amazon.com/Accoutrements-11761-Yodelling-Pickle/dp/B0010VS078/ref=sr_1_1'
CART = 'https://www.amazon.com/gp/cart/view.html/ref=dp_atch_dss_cart'

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 33500    # 最低金額


def l(str):
    print(
        "%s : %s" %
        (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))


def login(b):
    b.get(HOME)
    time.sleep(0.5)
    b.find_element_by_id("nav-link-accountList").click()
    b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
    b.find_element_by_id('continue').click()
    b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    b.find_element_by_id('signInSubmit').click()
    l('Login Info: {}'.format(b.find_element_by_id("nav-link-accountList").text))


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument("headless")

    try:
        b = webdriver.Chrome('./chromedriver', chrome_options=options)
        b.implicitly_wait(10)
    except Exception as e:
        l('Failed to open browser: {}'.format(e))
        exit()

    try:
        login(b)
    except Exception as e:
        l('Error Could not login: {}'.format(e))
        exit(1)

    try:
        found = False
        count = 0
        while(found == False):
            count += 1
            if (count > 3):
                break
            try:
                b.get(ITEM_URL)
                myDynamicElement = b.find_element_by_id("merchant-info")
                found = True
            except Exception as e:
                l("Could not find merchant info: {}".format(e))
        if found is False:
            raise Exception("Could Not Find Merchant")

        l('Got Merchant: {}'.format(myDynamicElement.text))
        shop = myDynamicElement.text.find(ACCEPT_SHOP)
        if shop == -1:
            raise Exception("Amazon is not the seller")
        b.find_element_by_id("add-to-cart-button").click()
        time.sleep(0.3)
        # b.implicitly_wait(5)
        b.get(CART)
        # time.sleep(0.5)
        sub_total = b.find_element_by_id(
            "sc-subtotal-label-buybox").text + b.find_element_by_id("sc-subtotal-amount-buybox").text
        l('Subtotal: {}'.format(sub_total))
        # time.sleep(0.5)
        b.refresh()
    except Exception as e:
        l('Could not get Merchant: {}'.format(e))
    finally:
        b.close()

    l('ALL DONE.')
    # shop = shop.split('が販売')[0].split('この商品は、')[1]

    # if ACCEPT_SHOP not in shop:
    #     raise Exception("not Amazon.")

    # カードに入れる
    # b.find_element_by_id('add-to-cart-button').click()
    # break
    # except:
    #     time.sleep(60)
    #     b.refresh()

    # b.find_element_by_name('proceedToCheckout').click()

    # try:
    #     b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
    #     b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    #     b.find_element_by_id('signInSubmit').click()
    # except:
    #     l('LOGIN PASS.')
    #     pass

    # p = b.find_element_by_css_selector('td.grand-total-price').text
    # if int(p.split(' ')[1].replace(',', '')) > LIMIT_VALUE:
    #     l('PLICE IS TOO LARGE.')
    #     continue

    # b.find_element_by_name('placeYourOrder1').click()
    # break
