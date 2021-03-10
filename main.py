import re
from selenium import webdriver
from selenium.common import exceptions
from Config import Configuration
import time
import threading
import os

class NikeBot:
    def __init__(self, product_url, config, driver_path="/sbin/chromedriver"):
        self.product_link = product_url
        self.config = config

        self.driver = webdriver.Chrome(driver_path)
        self.driver.get(product_url)

    def get_button(self):
        buttons = self.driver.find_elements_by_css_selector("button[data-qa='size-dropdown']")

        for button in buttons:
            if (re.match(f"M {self.config['size']}", button.text)):
                return button
        return None

    def add_to_cart(self):
        button = None
        for i in range(50):
            button = self.get_button()
            if button is not None:
                break
        else:
            print("No button")
            return False
        button.click()

        self.driver.find_element_by_css_selector("button[data-qa='add-to-cart']").click()
        return True

    def checkout(self):
        self.driver.get("https://www.nike.com/checkout/tunnel")
        while True:
            try:
                self.driver.find_element_by_id("qa-guest-checkout").click()
                break
            except exceptions.ElementNotInteractableException:
                print("not desktop")
            try:
                self.driver.find_element_by_id("qa-guest-checkout-mobile").click()
                break
            except exceptions.ElementNotInteractableException:
                print("waiting for button")

        self.wait_for_id("firstName").send_keys(self.config["f_name"])
        self.driver.find_element_by_id("lastName").send_keys(self.config["l_name"])

        self.driver.find_element_by_id("addressSuggestionOptOut").click()

        self.wait_for_id("address1").send_keys(self.config["street"])
        self.driver.find_element_by_id("city").send_keys(self.config["city"])
        self.driver.find_element_by_id("state").send_keys(self.config["state"])
        self.driver.find_element_by_id("postalCode").send_keys(self.config["postal_code"])

        self.driver.find_element_by_id("email").send_keys(self.config["email"])
        self.driver.find_element_by_id("phoneNumber").send_keys(self.config["phone"])
        self.driver.find_element_by_class_name("saveAddressBtn").click()
        self.wait_for_class("continuePaymentBtn").click()
        self.wait_for_xpath_text("/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[3]/div/button", "CONTINUE TO PAYMENT").click()
        while True:
            try:
                btn = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[2]/div/div[3]/div/button")
                if btn.text == "CONTINUE TO PAYMENT":
                    btn.click()
                else:
                    break
            except:
                break

        time.sleep(1.5)

        frame = self.wait_for_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/iframe')
        self.driver.switch_to.frame(frame)


        self.wait_for_xpath('//*[@id="creditCardNumber"]').send_keys(self.config["number"][:8])
        self.wait_for_xpath('//*[@id="expirationDate"]').send_keys(self.config["date"])
        self.wait_for_xpath('//*[@id="creditCardNumber"]').send_keys(self.config["number"][8:13])
        self.wait_for_xpath('//*[@id="cvNumber"]').send_keys(self.config["cvv"])
        self.wait_for_xpath('//*[@id="creditCardNumber"]').send_keys(self.config["number"][13:])

        # self.driver.switch_to.window("main")
        # self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[5]/button").click()
        self.driver.switch_to.parent_frame()
        self.driver.find_element_by_xpath('//*[@id="payment"]/div/div[1]/div[2]/div[5]/button').click()
        while True:
            try:
                self.wait_for_class('placeOrderBtn').click()
                break
            except exceptions.ElementNotInteractableException:
                pass

    def wait_for_id(self, id):
        while True:
            try:
                return self.driver.find_element_by_id(id)
            except:
                pass

    def wait_for_class(self, class_):
        while True:
            try :
                return self.driver.find_element_by_class_name(class_)
            except:
                pass

    def wait_for_xpath(self, path):
        while True:
            try :
                return self.driver.find_element_by_xpath(path)
            except:
                pass

    def wait_for_xpath_text(self, path, text):
        while True:
            try:
                btn = self.driver.find_element_by_xpath(path)
                if btn.text == text:
                    return btn
            except:
                pass

    def wait_for_css_selector(self, selector):
        while True:
            try :
                return self.driver.find_element_by_css_selector(selector)
            except:
                pass

configs = [
    Configuration("7", "Samuel", "Flanzer", "217 Central st", "Acton", "Massachusetts", "01720", "sam@dash-cloud.com",
                  "9783399511", "4270825019009088", "1023", "123"),
    Configuration("7", "Luis", "Hall", "7993 Temple Ave", "Norman", "Oklahoma", "73072", "test@gmail.com",
                           "7145527650", "372076304520182", "1023", "123")
]
current_index = 0

def run_instance():
    global current_index
    b = NikeBot("https://www.nike.com/launch/t/air-max-3-hot-lime", configs[current_index])
    current_index = (current_index + 1) % len(configs)
    while not b.add_to_cart():
        print("refreshing")
        b.driver.refresh()
    b.checkout()
    input()

num_instances = 2

for i in range(num_instances):
    threading.Thread(target=run_instance).start()
