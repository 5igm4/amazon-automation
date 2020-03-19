import os
import time

from logger import l
from selenium.common.exceptions import NoSuchElementException

LOGIN_ID = os.environ.get('UUID', None)
LOGIN_PASSWORD = os.environ.get('PASS', None)

# https://www.amazon.com/Accoutrements-11761-Yodelling-Pickle/dp/B0010VS078/ref=sr_1_1
ITEM_URL = os.environ.get('ITEM', None)

HOME = 'https://www.amazon.com/'
CART = 'https://www.amazon.com/gp/cart/view.html/ref=dp_atch_dss_cart'

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 100.00


def login(b):
    # Tries to log you in

    l('Attempting to sign-in')
    b.get(HOME)
    # time.sleep(0.5)
    b.find_element_by_id("nav-link-accountList").click()
    b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
    b.find_element_by_id('continue').click()
    b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    b.find_element_by_id('signInSubmit').click()
    l('Successfully signed-in as: {}'.format(b.find_element_by_id("nav-link-accountList").text.split(' ')[1].split('\n')[0]))


def check_item_stock(b):
    """Checks if item is unavailable

    Refreshes every 10 seconds until item is in-stock
    """

    outOfStock = True
    while(outOfStock == True):
        try:
            b.get(ITEM_URL)
            b.find_element_by_id("outOfStock")
            l("Item is outOfStock")
            b.refresh()
        except NoSuchElementException as e:
            try:
                b.find_element_by_id("merchant-info")
                l("Item is in-stock!")
                outOfStock = False
                continue
            except NoSuchElementException as e:
                time.sleep(1)
                b.get(ITEM_URL)
                continue
    return


def verify_seller(b):
    # verify that the seller is (fulfilled by) Amazon

    element = b.find_element_by_id("merchant-name")
    shop = element.text.find(ACCEPT_SHOP)
    if shop == -1:
        raise Exception("Amazon is not the seller")


def add_to_cart(b):
    # adds the item to our cart

    try:
        # check if amazon wants us to sub
        b.find_element_by_id("oneTimeBuyBox").click()
    except:
        pass

    b.find_element_by_id("add-to-cart-button").click()
    # time.sleep(0.3)


def print_subtotal(b):
    """Goes to cart and prints the subtotal

    Since page navigates to cart this also preps
    for checkout.
    """

    b.get(CART)
    # time.sleep(0.5)
    sub_total = b.find_element_by_id(
        "sc-subtotal-label-buybox").text + b.find_element_by_id("sc-subtotal-amount-buybox").text
    l('Subtotal: {}'.format(sub_total))
