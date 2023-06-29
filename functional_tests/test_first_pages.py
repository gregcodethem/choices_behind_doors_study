import time

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .base import (
    BaseTest,
    get_profile_by_username
)

class VisitorClicksThroughFirstPages(BaseTest):


    def test_click_through(self):
        # user accesses website and logs in
        self.browser.get(self.live_server_url)

        # Login screen appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        login_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn('Login', login_title)

        # User logs in
        self.login()
        time.sleep(0.5)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )

        # Sees first page: participant information sheet
        page_one_title = self.browser.find_element_by_tag_name(
            'h2').text
        self.assertIn("Participant Information Sheet", page_one_title)

        # Sees continue to next page at bottom
        continue_message = self.browser.find_element_by_id(
            'go_to_consent_questions').text
        self.assertIn("Continue to next page", continue_message)

        # User clicks continue and sees second page:
        continue_link = self.browser.find_element_by_id(
            'go_to_consent_questions')
        continue_link.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )

        consent_form_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn("CONSENT FORM", consent_form_title)

        # User clicks that they consent to the terms
        consent_link_text = self.browser.find_element_by_id(
            'go_to_prelim_one'
        ).text
        self.assertIn("I consent", consent_link_text)
        consent_link = self.browser.find_element_by_id(
            'go_to_prelim_one'
        )
        consent_link.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'p'))
        )

        # User sees the third page with a welcome message
        welcome_message = self.browser.find_element_by_tag_name('p').text
        self.assertIn("Welcome to the Monty Hall Game", welcome_message)

        # User sees the continue message and clicks on it
        continue_message_on_third_page = self.browser.find_element_by_id(
            "go_to_prelim_one_part_b"
        ).text
        self.assertIn("Continue", continue_message_on_third_page)

        continue_link_on_third_page = self.browser.find_element_by_id(
            "go_to_prelim_one_part_b"
        )
        continue_link_on_third_page.click()

        # User sees the fourth page
        first_line_on_fourth_page = self.browser.find_element_by_tag_name('p').text
        self.assertIn("You will now have", first_line_on_fourth_page)

        # User sees another continue message and clicks on it
        continue_message_on_fourth_page = self.browser.find_element_by_id(
            "go_to_prelim_two"
        ).text
        self.assertIn("Continue", continue_message_on_third_page)

        continue_link_on_fourth_page = self.browser.find_element_by_id(
            "go_to_prelim_two"
        )
        continue_link_on_fourth_page.click()

        #user sees countdown, then 3 by 3 grid
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-1'))
        )
        small_box_list = self.browser.find_elements_by_class_name(
            "col-sm-1"
        )
        number_of_small_boxes = len(small_box_list)
        self.assertEqual(number_of_small_boxes,9)

        # User cannot see a message displayed saying: "Can you remember the pattern from before?"
        try:
            remember_pattern_message = self.browser.find_element_by_id(
            "final_pattern_message"
        )
            remember_pattern_message_present = True
        except NoSuchElementException:
            remember_pattern_message_present = False

        self.assertFalse(
            remember_pattern_message_present,
            "The message above the grid should not be present"
        )

        # User remembers the pattern and then a blank grid appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_pattern_message'))
        )

        # Above the grid should be a message
        remember_pattern_message_actual = self.browser.find_element_by_id(
            "final_pattern_message"
        ).text
        self.assertIn(
            "Can you remember the pattern from before?",
            remember_pattern_message_actual
        )

        # The user should see a message asking them to
        # have another go at remembering the pattern

        link_to_do_practise_memory_game_again = self.browser.find_element_by_id(
            "go_to_prelim_two_again"
        )
        continue_message = link_to_do_practise_memory_game_again.text
        self.assertIn("Have another go at remembering the pattern", continue_message)

        # The user clicks on the link
        link_to_do_practise_memory_game_again.click()

        # The user should see text saying, this is what you chose
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'feedback_text'))
        )
        feedback_text_message = self.browser.find_element_by_id(
            'feedback_text'
        ).text

        self.assertIn('This is what you chose:', feedback_text_message)



