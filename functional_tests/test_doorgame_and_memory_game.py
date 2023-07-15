import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .base import (
    BaseTest,
    get_profile_by_username,
    attribute_has_changed,
)

class LayoutTest(BaseTest):

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

        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        # James can see a door in position 1
        door_one = self.browser.find_element_by_id('door1')
        image_door_one_before_click = door_one.get_attribute('src')

        # Check that this door is the normal door and is not red
        normal_door_url = self.live_server_url + '/static/doorgame/door.png'
        self.assertEqual(
            image_door_one_before_click,
            normal_door_url
        )

        # James can chose a door and clicks on door one
        door_number = 'door1'
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, door_number))
        )
        door_to_choose = self.browser.find_element_by_id(door_number)
        door_to_choose.click()

        # wait for the image to change
        WebDriverWait(self.browser, 10).until(
            attribute_has_changed((By.ID, "door1"), 'src', image_door_one_before_click)
        )

        # Now the door has changed
        door_one = self.browser.find_element_by_id('door1')
        image_door_one_after_click = door_one.get_attribute('src')
        self.assertNotEqual(
            image_door_one_before_click,
            image_door_one_after_click)

        # It appears as red
        red_door_url = self.live_server_url + '/static/doorgame/red_door.png'
        self.assertEqual(
            image_door_one_after_click,
            red_door_url
        )

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'result_of_first_door_choice'))
        )

        # User sees message that they've chosen a door
        first_door_chosen_message = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('The result of your door choice', first_door_chosen_message)

        # James can still see which door they've chosen
        # Now the door has changed
        door_one_result_page = self.browser.find_element_by_id('door1')
        image_door_one_result_page = door_one_result_page.get_attribute('src')
        self.assertEqual(
            image_door_one_result_page,
            red_door_url
        )

        # their door choice is saved
        # user logs out
        self.logout()
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        # ------- Door 2-------
        # Ozen then logs in
        self.user_goes_straight_to_first_door_game_via_memory_game(
            user_identifier="Ozen"
        )
        # sees text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        # Ozen can chose a door
        door_number = 'door2'
        self.user_chooses_a_door(door_number)

        first_door_chosen_message = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('The result of your door choice', first_door_chosen_message)

        # Ozen can still see which door they've chosen
        # Now the door has changed
        door_two_result_page = self.browser.find_element_by_id('door2')
        image_door_two_result_page = door_two_result_page.get_attribute('src')
        self.assertEqual(
            image_door_two_result_page,
            red_door_url
        )
        # Ozen logs out
        self.logout()

        # ------- Door 3 ------
        # Bob logs in
        self.user_goes_straight_to_first_door_game_via_memory_game(
            user_identifier="Bob"
        )
        # see text welcome page
        game_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to the door game', game_title)

        # Bob can chose a door
        door_number = 'door3'
        self.user_chooses_a_door(door_number)

        first_door_chosen_message = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('The result of your door choice', first_door_chosen_message)

        # Now the door has changed
        door_three_result_page = self.browser.find_element_by_id('door3')
        image_door_three_result_page = door_three_result_page.get_attribute('src')
        self.assertEqual(
            image_door_three_result_page,
            red_door_url
        )
        # Bob logs out
        self.logout()


    def test_multiple_users_can_have_turns(self):
        # John comes to site
        self.user_goes_straight_to_first_door_game_via_memory_game()

        # John notices that her account has a unique URL
        john_game_url = self.browser.current_url
        self.assertRegex(john_game_url, '/user/.+')

        self.user_chooses_a_door("door1")
        # their door choice is saved
        # user logs out
        self.logout()

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ozen visits the home page.
        self.user_goes_straight_to_first_door_game_via_memory_game(
            user_identifier="Ozen"
        )
        # Ozen gets her own unique URL
        ozen_game_url = self.browser.current_url
        self.assertRegex(ozen_game_url, '/user/.+')
        self.assertNotEqual(ozen_game_url, john_game_url)

        self.user_chooses_a_door("door2")
        # this url is also has user as a prefix
        ozen_result_url = self.browser.current_url
        self.assertRegex(ozen_result_url, '/user/.+')

        # their door choice is saved
        # user logs out
        self.logout()



class SecondChoiceTest(BaseTest):

    def test_user_can_keep_door_choice_and_get_pattern_again(self):
        # John comes to site
        self.user_goes_straight_to_first_door_game_via_memory_game()

        self.user_chooses_a_door("door1")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'monty_speech_bubble'))
        )
        # John sees message that they can change door
        new_choice_message = self.browser.find_element_by_id(
            'monty_speech_bubble').text
        self.assertIn("I am revealing one of the two goats.", new_choice_message)

        # John can see a goat in either door two or door three
        goat_two = self.browser.find_elements_by_id(
            'open_door_goat2'
        )
        goat_three = self.browser.find_elements_by_id(
            'open_door_goat3'
        )
        self.assertTrue(
            len(goat_three) > 0 or len(goat_two) > 0,
            "Neither 'open_door_goat3' nor 'open_door_goat2' was found"
        )
        # check that there is no goat image for door 1:
        goat_one = self.browser.find_elements_by_id(
            'open_door_goat1'
        )
        self.assertTrue(
            len(goat_one) == 0,
            "'open_door_goat1' was found"
        )


        # John can see option to keep or change their choice
        keep_door_link = self.browser.find_element_by_id('keep_door_link')
        keep_door_text = keep_door_link.text
        self.assertEqual(keep_door_text,'Stick with door 1',msg="keep door text not found or incorrect")

        change_door_link = self.browser.find_element_by_id('change_door_link')
        change_door_text = change_door_link.text
        self.assertTrue(
            change_door_text=="Switch to door 2" or change_door_text=="Switch to door 3",
            f"Change door text is incorrect:{change_door_text}"
        )

        # John choses to keep their door choice
        keep_door_link.click()

        # When John has done the process the required number
        # of times, he then sees a regret page
        # John sees a regret page:
        regret_message = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('To what extent would you experience regret', regret_message)

        # They click on the number 1
        regret_one = self.browser.find_element_by_id('regret_one')
        regret_one.click()

        # Then they click submit
        submit_button = self.browser.find_element_by_id('complete-the-survey')
        submit_button.click()


        # John sees the grid from before

        final_pattern_message = self.browser.find_element_by_id(
            'final_pattern_message').text
        self.assertIn(
            'Can you remember the pattern from before?', final_pattern_message
        )
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'div_box_1'))
        )
        # John sees blank boxes that they can click
        box_1 = self.browser.find_element_by_id('div_box_1')
        box_2 = self.browser.find_element_by_id('div_box_2')
        box_3 = self.browser.find_element_by_id('div_box_3')

        box_1.click()
        box_2.click()
        box_3.click()

        # !!!! in this version of the FT, the user won't play again
        # I need another FT, where they play twice, then
        # a code block equivalent to this will go there
        # user goes back to first screen
        play_again_link = self.browser.find_element_by_id(
            'play_again_link')
        play_again_link.click()

        # Note if they choose the wrong number of doors,
        # At present the blank boxes will just appear again

        # John should see text for his final door result
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_choice_message'))
        )

        final_door_message = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('The result of your final door choice', final_door_message)


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
        # John comes to site
        self.user_goes_straight_to_first_door_game_via_memory_game()

        self.user_chooses_a_door("door1")

        # John sees option that they can change door
        change_door_link = self.browser.find_element_by_id('change_door_link')
        change_door_text = change_door_link.text
        self.assertTrue(
            change_door_text == "Switch to door 2" or change_door_text == "Switch to door 3",
            f"Change door text is incorrect:{change_door_text}"
        )

        # User choses to keep their door choice
        change_door_link.click()

        # When John has done the process the required number
        # of times, he then sees a regret page
        # John sees a regret page:
        regret_message = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('To what extent would you experience regret', regret_message)

        # They click on the number 1
        regret_one = self.browser.find_element_by_id('regret_one')
        regret_one.click()

        # Then they click submit
        submit_button = self.browser.find_element_by_id('complete-the-survey')
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_pattern_message'))
        )

        # John sees the grid from before
        final_pattern_message = self.browser.find_element_by_id(
            'final_pattern_message').text
        self.assertIn(
            'Can you remember the pattern from before?', final_pattern_message
        )
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'div_box_1'))
        )
        # John sees blank boxes that they can click
        box_1 = self.browser.find_element_by_id('div_box_1')
        box_2 = self.browser.find_element_by_id('div_box_2')
        box_3 = self.browser.find_element_by_id('div_box_3')

        box_1.click()
        box_2.click()
        box_3.click()

        # !!!! in this version of the FT, the user won't play again
        # I need another FT, where they play twice, then
        # a code block equivalent to this will go there
        # user goes back to first screen
        play_again_link = self.browser.find_element_by_id(
            'play_again_link')
        play_again_link.click()

        # Note if they choose the wrong number of doors,
        # At present the blank boxes will just appear again

        # John should see text for his final door result
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_choice_message'))
        )

        final_door_message = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('The result of your final door choice', final_door_message)

        self.logout()
