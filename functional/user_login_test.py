import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class UserLoginTests(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = os.getenv("BASE_URL", "")
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_login_email_required(self):
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        assert self.driver.title == 'Login - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if redirected to login

        self.driver.find_element(by=By.ID, value="submit").click()  # submit form
        required = self.driver.find_element(by=By.ID, value="email").get_attribute("required")
        assert required == "true"  # check if email is required

        assert self.driver.title == "Login - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if not redirected

    def test_login_user_doesnt_exist(self):
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        assert self.driver.title == 'Login - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if redirected to login

        self.driver.find_element(by=By.ID, value="email").send_keys("gg@gg.gg")
        self.driver.find_element(by=By.ID, value="submit").click()  # submit form

        assert self.driver.title == "Login - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if not redirected
        assert self.driver.find_element(by=By.ID, value="alert-info").is_displayed()

    def test_login(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))
        self.driver.find_element(by=By.ID, value="username").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="name").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="surname").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("aaa@bbb.ccc")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        self.driver.get(os.path.join(self.BASE_URL, "login"))

        assert self.driver.title == 'Login - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if redirected to login

        self.driver.find_element(by=By.ID, value="email").send_keys("aaa@bbb.ccc")
        self.driver.find_element(by=By.ID, value="submit").click()  # submit form
        assert self.driver.title == "Paint Drying"
        assert self.driver.current_url == self.BASE_URL  # check if redirected

        self.driver.find_element(by=By.LINK_TEXT, value="Logout").click()
