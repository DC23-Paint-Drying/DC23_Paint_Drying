import os
import unittest

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


class MainPageTestsLoggedOut(unittest.TestCase):
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

    def test_login_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Login").click()  # click link to go to login form

        assert self.driver.title == 'Login - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "login")  # check if redirected to login

    def test_register_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Register").click()  # click link to go to register form

        assert self.driver.title == 'Register - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "register")  # check if redirected to register

    def test_logout_link(self):
        self.driver.get(self.BASE_URL)

        logout_link = self.driver.find_elements(by=By.LINK_TEXT, value="Logout")

        assert len(logout_link) == 0

    def test_logout_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "logout"))

        assert self.driver.title == 'Unauthorized - Paint Drying'

    def test_order_subscription_link(self):
        self.driver.get(self.BASE_URL)

        order_subscription_link = self.driver.find_elements(by=By.LINK_TEXT, value="Order subscription")

        assert len(order_subscription_link) == 0

    def test_order_subscription_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "subscribe"))

        assert self.driver.title == 'Unauthorized - Paint Drying'

    def test_edit_user_subscription_link(self):
        self.driver.get(self.BASE_URL)

        edit_user_subscription_link = self.driver.find_elements(by=By.LINK_TEXT, value="Edit User Subscription")

        assert len(edit_user_subscription_link) == 0

    def test_edit_user_subscription_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "edit-subscription"))

        assert self.driver.title == 'Unauthorized - Paint Drying'

    def test_edit_user_data_link(self):
        self.driver.get(self.BASE_URL)

        edit_user_link = self.driver.find_elements(by=By.LINK_TEXT, value="Edit User Data")

        assert len(edit_user_link) == 0

    def test_edit_user_data_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "edit-profile"))

        assert self.driver.title == 'Unauthorized - Paint Drying'

    def test_order_packets_link(self):
        self.driver.get(self.BASE_URL)

        order_packets_link = self.driver.find_elements(by=By.LINK_TEXT, value="Order packets")

        assert len(order_packets_link) == 0

    def test_order_packets_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "order-packets"))

        assert self.driver.title == 'Unauthorized - Paint Drying'


class MainPageTestsLoggedIn(unittest.TestCase):
    BASE_URL = None
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.register_user()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
    def register_user(cls):
        cls.BASE_URL = os.getenv("BASE_URL")
        cls.driver.get(os.path.join(cls.BASE_URL, "register"))
        cls.driver.find_element(by=By.ID, value="username").send_keys("xxx")
        cls.driver.find_element(by=By.ID, value="name").send_keys("xxx")
        cls.driver.find_element(by=By.ID, value="surname").send_keys("xxx")
        cls.driver.find_element(by=By.ID, value="age").send_keys("99")
        cls.driver.find_element(by=By.ID, value="email").send_keys("x@x.x")
        cls.driver.find_element(by=By.ID, value="gender-1").click()
        cls.driver.implicitly_wait(0.5)
        element = cls.driver.find_element(by=By.ID, value="submit")
        cls.driver.execute_script("arguments[0].click();", element)

    def setUp(self):
        display = Display(visible=0, size=(800, 800))
        display.start()
        chromedriver_autoinstaller.install()
        self.BASE_URL = os.getenv("BASE_URL")
        self.driver = webdriver.Chrome()

        self.driver.get(os.path.join(self.BASE_URL, "login"))
        self.driver.find_element(by=By.ID, value="email").send_keys("x@x.x")
        self.driver.find_element(by=By.ID, value="submit").click()

    def tearDown(self):
        self.driver.close()

    def test_main(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying'

    def test_login_link(self):
        self.driver.get(self.BASE_URL)

        login_link = self.driver.find_elements(by=By.LINK_TEXT, value="Login")

        assert len(login_link) == 0

    def test_login_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "login"))

        assert self.driver.title == 'Login - Paint Drying'

    def test_register_link(self):
        self.driver.get(self.BASE_URL)

        register_link = self.driver.find_elements(by=By.LINK_TEXT, value="Register")

        assert len(register_link) == 0

    def test_register_link_unauthorized(self):
        self.driver.get(os.path.join(self.BASE_URL, "register"))

        assert self.driver.title == 'Register - Paint Drying'

    def test_order_subscription_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Order subscription")


    def test_edit_user_subscription_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Edit User Subscription").click()

        assert self.driver.title == 'Edit Subscription - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "edit-subscription")

    def test_edit_user_data_link(self):
        self.driver.get(self.BASE_URL)

        edit_user_data_link = self.driver.find_elements(by=By.LINK_TEXT, value="Edit User Data")

        assert len(edit_user_data_link) == 0

    def test_order_packets_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Order packets").click()

        assert self.driver.title == 'Order Packets - Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "order-packets")

    def test_logout_link(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.LINK_TEXT, value="Logout").click()

        assert self.driver.title == 'Paint Drying'
        assert self.driver.current_url == os.path.join(self.BASE_URL, "logout")
