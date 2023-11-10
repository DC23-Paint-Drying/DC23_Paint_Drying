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
        self.BASE_URL = self.BASE_URL = os.getenv("BASE_URL", "") + '/admin_panel'
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_main(self):
        self.driver.get(self.BASE_URL)
        assert self.driver.title == 'Paint Drying/Admin Panel'
    def test_send_mail(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.ID, value="suggest-services-label").click()

        assert self.driver.find_element(by=By.ID, value="notification").text == "Mails sent"
    def test_send_invoice(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.ID, value="send-invoice-label").click()

        assert self.driver.find_element(by=By.ID, value="notification").text == "Invoices sent"
    def test_send_generate_report(self):
        self.driver.get(self.BASE_URL)

        self.driver.find_element(by=By.ID, value="generate-report-label").click()

        assert self.driver.find_element(by=By.ID, value="notification").text == "Report generated"

