import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .base import BaseTest


class LoginTest(BaseTest):

    def test_login(self):
        # James accesses website and logs in
        self.browser.get(self.live_server_url)

        # Login screen appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        login_title = self.browser.find_element(
            By.TAG_NAME,
            'h2').text
        self.assertIn('Login', login_title)

        # James logs in
        self.login()
        time.sleep(3)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )

        # Sees first page: participant information sheet
        page_one_title = self.browser.find_element(
            By.TAG_NAME,
            'h2').text
        self.assertIn("Participant Information Sheet", page_one_title)
