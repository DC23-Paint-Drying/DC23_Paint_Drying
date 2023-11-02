import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class MainPageTests(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = os.getenv("BASE_URL")
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_main(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

    def test_register_link(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

        self.driver.find_element(by=By.LINK_TEXT, value="Register").click()        # click lint to go to register form

        assert self.driver.title == 'Register - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if redirected to register

    def test_order_subscription_link(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

        self.driver.find_element(by=By.LINK_TEXT, value="Order subscription").click()

        assert self.driver.title == 'Order Subscription - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "subscribe")

    def test_edit_user_subscription_link(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

        self.driver.find_element(by=By.LINK_TEXT, value="Edit User Subscription").click()

        assert self.driver.title == 'Edit Subscription - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "edit-subscription")
