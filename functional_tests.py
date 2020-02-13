from selenium import webdriver

import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_see_login_page(self):
        self.browser.get('http://localhost:8000/accounts/login')
        self.assertIn('Login', self.browser.title)

        # Enter username and password

        # click Login

        # see text welcome page

if __name__ == '__main__':
    unittest.main()
