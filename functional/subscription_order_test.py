import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class SubscriptionOrderTests(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = os.getenv("BASE_URL", "")
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_subscription_order(self):
        self.driver.get(os.path.join(self.BASE_URL, "subscribe"))

        assert self.driver.title == "Order Subscription - Paint Drying"

        self.driver.find_element(by=By.ID, value="email").send_keys("a@b.c")        # write email address to email field
        self.driver.find_element(by=By.ID, value="subscription_level-0").click()    # check bronze subscription
        self.driver.find_element(by=By.ID, value="submit").click()                  # submit form

        assert self.driver.title == "Paint Drying"
        assert self.driver.current_url == self.BASE_URL                             # check if redirected to main

    def test_subscription_order_return_to_main(self):
        self.driver.get(os.path.join(self.BASE_URL, "subscribe"))

        assert self.driver.title == "Order Subscription - Paint Drying"

        self.driver.find_element(by=By.LINK_TEXT, value="Main Page").click()        # click lint to return to main page

        assert self.driver.title == "Paint Drying"
        assert self.driver.current_url == self.BASE_URL

    def test_subscription_order_email_required(self):
        self.driver.get(os.path.join(self.BASE_URL, "subscribe"))

        assert self.driver.title == "Order Subscription - Paint Drying"

        self.driver.implicitly_wait(0.5)

        self.driver.find_element(by=By.ID, value="subscription_level-0").click()
        self.driver.find_element(by=By.ID, value="submit").click()

        required = self.driver.find_element(by=By.ID, value="email").get_attribute("required")
        assert required == "true"

        assert self.driver.title == "Order Subscription - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "subscribe")  # check if not redirected

    def test_subscription_order_sub_level_required(self):
        self.driver.get(os.path.join(self.BASE_URL, "subscribe"))

        assert self.driver.title == "Order Subscription - Paint Drying"

        self.driver.find_element(by=By.ID, value="email").send_keys("a@b.c")
        self.driver.find_element(by=By.ID, value="submit").click()

        assert self.driver.title == "Order Subscription - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "subscribe")
