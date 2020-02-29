from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self):


        # Enter username and password
        username_input_box = self.browser.find_element_by_id(
            'id_username')
        username_input_box.send_keys('greg')
        password_input_box = self.browser.find_element_by_id(
            'id_password')
        password_input_box.send_keys('Spain')
        # click Login
        password_input_box.send_keys(Keys.ENTER)
        time.sleep(1)

    def logout(self):
        logout_link = self.browser.find_element_by_id('logout_link_anchor')
        logout_link.click()
        time.sleep(2)

    def test_can_see_login_page(self):
        self.browser.get('http://localhost:8000/accounts/login')
        # Login screen appears
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        self.login()

        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        # user can see a door
        door1 = self.browser.find_element_by_id('door1')
        self.assertAlmostEqual(
            door1.location['x'] + door1.size['width'] / 2,
            100,
            delta=10
        )
        '''
        door2 = self.browser.find_element_by_id('door2')
        self.assertAlmostEqual(
            door2.location['x'] + door2.size['width'] / 2,
            300,
            delta=20
        )
        door3 = self.browser.find_element_by_id('door3')
        self.assertAlmostEqual(
            door3.location['x'] + door3.size['width'] / 2,
            480,
            delta=20
        )
        '''
        
        # user can chose a door
        # user clicks on door1
        door1.click()
        time.sleep(1)

        # User sees message that they've chosen door1
        chosen_message = self.browser.find_element_by_id(
            'chosen_message').text
        self.assertIn('You chose door1', chosen_message)

        # their door choice is saved

        # user logs out
        self.logout()

        # User choses another door
        door2 = self.browser.find_element_by_id('door2')
        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        #self.assertIn('Welcome to the door game', game_title)
        logged_out_message = self.browser.find_element_by_tag_name('p').text
        self.assertIn('You are not logged in', logged_out_message)
        # user clicks on door2
        door2.click()
        time.sleep(1)

        # User sees message that they've chosen door2
        chosen_message = self.browser.find_element_by_id(
            'chosen_message').text
        self.assertIn('You chose door2', chosen_message)

        # user logs out
        self.logout()

        # second user comes to the site

        # they chose a door

        # their choice is saved

        # the choice of user 1 is not saved


if __name__ == '__main__':
    unittest.main()
