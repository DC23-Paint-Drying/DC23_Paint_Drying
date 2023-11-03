import os
import unittest

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


class MainPageTests(unittest.TestCase):
    def setUp(self):
        display = Display(visible=0, size=(800, 800))
        display.start()
        chromedriver_autoinstaller.install()
        self.BASE_URL = os.getenv("BASE_URL")
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_main(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

    def test_register_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Register").click()        # click link to go to register form

        assert self.driver.title == 'Register - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if redirected to register

    def test_order_subscription_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Order subscription").click()

        assert self.driver.title == 'Order Subscription - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "subscribe")

    def test_edit_user_subscription_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Edit User Subscription").click()

        assert self.driver.title == 'Edit Subscription - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "edit-subscription")
