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

    def test_register(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))

        assert self.driver.title == 'Register - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if redirected to login

        self.driver.find_element(by=By.ID, value="username").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="name").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="surname").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("q@q.q")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        self.driver.implicitly_wait(0.5)
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        assert self.driver.title == "Paint Drying"
        assert self.driver.current_url == self.BASE_URL  # check if redirected

    def test_register_user_exists(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))

        assert self.driver.title == 'Register - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if redirected to login

        self.driver.find_element(by=By.ID, value="username").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="name").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="surname").send_keys("qqq")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("q@q.q")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        self.driver.implicitly_wait(0.5)
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        assert self.driver.title == "Register - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if not redirected
        assert self.driver.find_element(by=By.ID, value="alert-info").is_displayed()
