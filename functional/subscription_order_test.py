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
        self.driver.get(os.path.join(self.BASE_URL, "register"))
        self.driver.find_element(by=By.ID, value="username").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="name").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="surname").send_keys("aaa")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("a@a.a")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        self.driver.implicitly_wait(0.5)
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        self.driver.implicitly_wait(0.5)
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        self.driver.find_element(by=By.ID, value="email").send_keys("a@a.a")
        self.driver.find_element(by=By.ID, value="submit").click()  # submit form

        self.driver.get(os.path.join(self.BASE_URL, "edit-subscription"))
        assert self.driver.title == "Edit Subscription - Paint Drying"

        self.driver.find_element(by=By.ID, value="subscription_level-0").click()    # check bronze subscription
        self.driver.find_element(by=By.ID, value="submit").click()                  # submit form

        assert self.driver.title == "Additional Services - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "propose-additional-services")                             # check if redirected to propose additional services

    def test_subscription_order_return_to_main(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))
        self.driver.find_element(by=By.ID, value="username").send_keys("bbb")
        self.driver.find_element(by=By.ID, value="name").send_keys("bbb")
        self.driver.find_element(by=By.ID, value="surname").send_keys("bbb")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("b@b.b")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        self.driver.implicitly_wait(0.5)
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        self.driver.implicitly_wait(0.5)
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        self.driver.find_element(by=By.ID, value="email").send_keys("b@b.b")
        self.driver.find_element(by=By.ID, value="submit").click()  # submit form

        self.driver.get(os.path.join(self.BASE_URL, "edit-subscription"))

        self.driver.find_element(by=By.LINK_TEXT, value="Strona główna").click()        # click link to return to main page

        assert self.driver.title == "Paint Drying"
        assert self.driver.current_url == self.BASE_URL

    def test_subscription_order_sub_level_required(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))
        self.driver.find_element(by=By.ID, value="username").send_keys("ddd")
        self.driver.find_element(by=By.ID, value="name").send_keys("ddd")
        self.driver.find_element(by=By.ID, value="surname").send_keys("ddd")
        self.driver.find_element(by=By.ID, value="age").send_keys(11)
        self.driver.find_element(by=By.ID, value="email").send_keys("d@d.d")
        self.driver.find_element(by=By.ID, value="gender-1").click()
        self.driver.implicitly_wait(0.5)
        element = self.driver.find_element(by=By.ID, value="submit")  # submit form
        self.driver.execute_script("arguments[0].click();", element)

        self.driver.implicitly_wait(0.5)
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        self.driver.find_element(by=By.ID, value="email").send_keys("d@d.d")
        self.driver.find_element(by=By.ID, value="submit").click()  # submit form

        self.driver.get(os.path.join(self.BASE_URL, "edit-subscription"))

        self.driver.find_element(by=By.ID, value="submit").click()

        assert self.driver.title == "Edit Subscription - Paint Drying"
        assert self.driver.current_url == os.path.join(self.BASE_URL, "edit-subscription")
