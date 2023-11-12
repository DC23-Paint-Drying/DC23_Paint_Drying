import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class ListGdriveFilesTests(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = os.getenv("BASE_URL", "")
        self.driver = webdriver.Chrome()
        self.driver.get(self.BASE_URL + 'list_gdrive_files')

    def tearDown(self):
        self.driver.close()

    def test_page(self):
        assert self.driver.title == 'Paint Drying/Google Drive Files'

    def test_back_link(self):
        self.driver.find_element(by=By.LINK_TEXT, value="Back").click()
        assert self.driver.title == 'Paint Drying/Admin Panel'

    def test_main_page_link(self):
        self.driver.find_element(by=By.LINK_TEXT, value="Main Page").click()
        assert self.driver.title == 'Paint Drying'

