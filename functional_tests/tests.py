from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

test_login_data = {
    "Greg": {"username": "greg", "password": "Spain"},
    "Ozen": {"username": "ozen", "password": "Russia432"}
}

class BaseTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self, user_identifier="Greg"):
        # Enter username and password
        username_input_box = self.browser.find_element_by_id(
            'id_username')
        user_login_info = test_login_data[user_identifier]
        username = user_login_info["username"]
        password = user_login_info["password"]
        username_input_box.send_keys(
            username)
        password_input_box = self.browser.find_element_by_id(
            'id_password')
        password_input_box.send_keys(password)
        # click Login
        password_input_box.send_keys(Keys.ENTER)
        time.sleep(2)

    def logout(self):
        logout_link = self.browser.find_element_by_id('logout_link_anchor')
        logout_link.click()
        time.sleep(2)

    def user_clicks_through_memory_game(self):
        memory_title = self.browser.find_element_by_tag_name('h2').text
        
        # user can go to door game
        go_to_door_game = self.browser.find_element_by_id('go_to_door_game')
        go_to_door_game.click()
        time.sleep(1)

    def user_chooses_a_door(self, door_number):
        # door_number must be string

        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        time.sleep(2)
        
        # user can chose a door
        door1 = self.browser.find_element_by_id(door_number)
        # user clicks on door1
        door1.click()
        time.sleep(1)

        # User sees message that they've chosen door1
        chosen_message = self.browser.find_element_by_id(
            'chosen_message').text
        self.assertIn('You chose '+ door_number, chosen_message)



class NewVisitorTest(BaseTest):

    def test_layout(self):
        self.browser.get('http://localhost:8000/accounts/login')
        # Login screen appears
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        self.login()

        # sees memory game
        memory_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Can you remember these dots?', memory_title)

        # user can go to door game
        go_to_door_game = self.browser.find_element_by_id('go_to_door_game')
        go_to_door_game.click()

        time.sleep(1)
        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        time.sleep(2)
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

class DifferentChoiceTest(BaseTest):

    def test_user_can_choose_different_doors(self):
        self.browser.get('http://localhost:8000/accounts/login')
        # Login screen appears
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        
        self.login()

        self.user_clicks_through_memory_game()

        self.user_chooses_a_door("door1")
        # their door choice is saved
        # user logs out
        self.logout()


        # ------- Door 2-------
        # User logs in

        self.login()
        self.user_clicks_through_memory_game()
        self.user_chooses_a_door("door2")

        # user logs out
        self.logout()

        # ------- Door 3 ------
        # User logs in

        self.login()
        self.user_clicks_through_memory_game()
        
        self.user_chooses_a_door("door3")
        # user logs out
        self.logout()

    def test_multiple_users_can_have_turns(self):
        # first user comes to site
        self.browser.get('http://localhost:8000/accounts/login')
        self.login()

        # He notices that her account has a unique URL
        greg_game_url = self.browser.current_url
        self.assertRegex(greg_game_url, '/user/.+')

        self.user_clicks_through_memory_game()
        self.user_chooses_a_door("door1")
        # their door choice is saved
        # user logs out
        self.logout()

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ozen visits the home page.  
        self.browser.get('http://localhost:8000/accounts/login')

        self.login("Ozen")
        # Ozen gets her own unique URL
        ozen_game_url = self.browser.current_url
        self.assertRegex(ozen_game_url, '/user/.+')
        self.assertNotEqual(ozen_game_url, greg_game_url)

        self.user_clicks_through_memory_game()
        self.user_chooses_a_door("door2")
        # this url is also has user as a prefix
        ozen_result_url = self.browser.current_url
        self.assertRegex(ozen_result_url, '/user/.+')

        # their door choice is saved
        # user logs out
        self.logout()
        

        # they login with different details


        # they chose a door

        # their choice is saved

        # the choice of user 1 is not saved




class SecondChoiceTest(BaseTest):

    def test_user_can_keep_door_choice_and_get_pattern_again(self):
        self.browser.get('http://localhost:8000/accounts/login')
        # Login screen appears
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        self.login()
        time.sleep(1)

        self.user_clicks_through_memory_game()
        self.user_chooses_a_door("door1")

        # User sees message that they can change door
        new_choice_message = self.browser.find_element_by_id(
            'new_choice_message').text
        self.assertIn("It's not door", new_choice_message)
        self.assertRegex(new_choice_message, '.*\d\.*')
        self.assertIn("You can change your choice", new_choice_message)

        # User can see option to keep or change their choice
        keep_door_link = self.browser.find_element_by_id('keep_door_link')
        change_door_link = self.browser.find_element_by_id('change_door_link')
        # User choses to keep their door choice
        keep_door_link.click()
        time.sleep(2)
        # User sees message that they chose to keep their door choice.
        final_choice_message = self.browser.find_element_by_id(
            'final_choice_message').text
        self.assertIn("You chose door1", final_choice_message)

        final_pattern_message = self.browser.find_element_by_id(
            'final_pattern_message').text
        self.assertIn(
            'Can you remember the pattern from before?', final_pattern_message
            )
        
        self.logout()

    def test_user_can_change_door_choice(self):
        self.browser.get('http://localhost:8000/accounts/login')
        # Login screen appears
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        self.login()
        self.user_clicks_through_memory_game()

        self.user_chooses_a_door("door1")
        # User sees message that they can change door
        new_choice_message = self.browser.find_element_by_id(
            'new_choice_message').text
        self.assertIn("It's not door", new_choice_message)
        self.assertRegex(new_choice_message, '.*\d\.*')
        self.assertIn("You can change your choice", new_choice_message)

        # User can see option to keep or change their choice
        keep_door_link = self.browser.find_element_by_id('keep_door_link')
        change_door_link = self.browser.find_element_by_id('change_door_link')
        # User choses to keep their door choice
        change_door_link.click()
        time.sleep(2)

        # User sees message that they chose to CHANGE their door choice.
        final_choice_message = self.browser.find_element_by_id(
            'final_choice_message').text
        self.assertIn("You chose door", final_choice_message)
        self.assertNotIn("You chose door1", final_choice_message)

        self.logout()

    