import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .base import (
    BaseTest,
    get_profile_by_username
)

class NewVisitorTest(BaseTest):

    def test_layout(self):
        # James accesses website and logs in
        self.browser.get(self.live_server_url)
        # Login screen appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        # James logs in
        self.login()
        time.sleep(0.5)

        # James has completed all the prelims and sees memory game
        # James sees countdown, then 3 by 3 grid

        first_real_memory_game_url = self.live_server_url + '/memory_game_initial_turn'

        self.browser.get(first_real_memory_game_url)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-1'))
        )
        small_box_list = self.browser.find_elements_by_class_name(
            "col-sm-1"
        )
        number_of_small_boxes = len(small_box_list)
        self.assertEqual(number_of_small_boxes, 9)

        # In the 3 by 3 grid there should be 3 dots
        dot_pics_with_dots = self.browser.find_elements_by_xpath('//img[@src="/static/doorgame/box_with_dot.png"]')
        number_of_dots = len(dot_pics_with_dots)
        self.assertEqual(number_of_dots, 3)

        # James cannot see a message displayed saying: "Can you remember the pattern from before?"
        try:
            remember_pattern_message = self.browser.find_element_by_id(
                "Welcome to the door game"
            )
            remember_pattern_message_present = True
        except NoSuchElementException:
            remember_pattern_message_present = False

        self.assertFalse(
            remember_pattern_message_present,
            "The message above the grid should not be present"
        )

        # user sees a box they can remember
        box_1 = self.browser.find_element_by_id('box_1')
        box_2 = self.browser.find_element_by_id('box_2')

        # James is automatically redirected to the door game
        time.sleep(2)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'door1'))
        )
        # user can see a door
        door1 = self.browser.find_element_by_id('door1')
        self.assertAlmostEqual(
            door1.location['x'] + door1.size['width'] / 2,
            300,
            delta=50
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

        # James accesses website, logs in and goes to the door game
        self.user_goes_straight_to_first_door_game_via_memory_game()

        self.user_chooses_a_door("door1")
        # their door choice is saved
        # user logs out
        self.logout()

        # ------- Door 2-------
        # User logs in
        self.user_goes_straight_to_first_door_game_via_memory_game()
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

        # user sees blank boxes that they can click
        box_1 = self.browser.find_element_by_id('box_1')
        box_2 = self.browser.find_element_by_id('box_2')

        box_1.click()

        # user goes back to first screen
        play_again_link = self.browser.find_element_by_id(
            'play_again_link')
        play_again_link.click()

        time.sleep(1)

        '''
        This doesn't work on the test db:
        saved_trials = Trials.objects.all()
        saved_memory_game_results = MemoryGame.objects.all()
        print(len(saved_memory_game_results))
        # check memory game saved
        saved_memory_game = MemoryGame.objects.last()
        #saved_memory_game = saved_memory_game_results[-1]
        saved_box_1 = saved_memory_game.box_1
        saved_box_2 = saved_memory_game.box_2
        self.assertEqual(saved_box_1, True)
        self.assertEqual(saved_box_2, False)
        '''

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
