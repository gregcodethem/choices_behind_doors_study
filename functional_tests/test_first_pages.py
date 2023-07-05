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

        # James clicks continue and sees second page:
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

        # James sees the third page with a welcome message
        welcome_message = self.browser.find_element_by_tag_name('p').text
        self.assertIn("Welcome to the Monty Hall Game", welcome_message)

        # James sees the continue message and clicks on it
        continue_message_on_third_page = self.browser.find_element_by_id(
            "go_to_prelim_one_part_b"
        ).text
        self.assertIn("Continue", continue_message_on_third_page)

        continue_link_on_third_page = self.browser.find_element_by_id(
            "go_to_prelim_one_part_b"
        )
        continue_link_on_third_page.click()

        # James sees the fourth page
        first_line_on_fourth_page = self.browser.find_element_by_tag_name('p').text
        self.assertIn("You will now have", first_line_on_fourth_page)

        # James sees another continue message and clicks on it
        continue_message_on_fourth_page = self.browser.find_element_by_id(
            "go_to_prelim_two"
        ).text
        self.assertIn("Continue", continue_message_on_third_page)

        continue_link_on_fourth_page = self.browser.find_element_by_id(
            "go_to_prelim_two"
        )
        continue_link_on_fourth_page.click()

        # James sees countdown, then 3 by 3 grid
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-1'))
        )
        small_box_list = self.browser.find_elements_by_class_name(
            "col-sm-1"
        )
        number_of_small_boxes = len(small_box_list)
        self.assertEqual(number_of_small_boxes,9)

        # In the 3 by 3 grid there should be 3 dots
        dot_pics_with_dots = self.browser.find_elements_by_xpath('//img[@src="/static/doorgame/box_with_dot.png"]')
        number_of_dots = len(dot_pics_with_dots)
        self.assertEqual(number_of_dots,3)

        # James cannot see a message displayed saying: "Can you remember the pattern from before?"
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

        # James remembers the pattern and then a blank grid appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_pattern_message'))
        )
        time.sleep(3)
        # Above the grid should be a message
        remember_pattern_message_actual = self.browser.find_element_by_id(
            "final_pattern_message"
        ).text
        self.assertIn(
            "Can you remember the pattern from before?",
            remember_pattern_message_actual
        )

        # James should see a message asking them to
        # continue to the next page
        time.sleep(2)
        link_to_feedback_first_go = self.browser.find_element_by_id(
            "play_again_link"
        )

        continue_message = link_to_feedback_first_go.get_attribute("value")
        self.assertIn("Continue to next page", continue_message)

        # James clicks on the link
        link_to_feedback_first_go.click()

        # James should see text saying, this is what you chose
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'feedback_text'))
        )
        feedback_text_message = self.browser.find_element_by_id(
            'feedback_text'
        ).text

        self.assertIn('This is what you chose:', feedback_text_message)

        # James should also see two nine by nine grids
        dot_pics_with_dots = self.browser.find_elements_by_xpath(
            '//img[@src="/static/doorgame/box_with_dot.png"]'
        )
        dot_pics_with_blanks = self.browser.find_elements_by_xpath(
            '//img[@src="/static/doorgame/box_empty.png"]'
        )
        number_of_pics_with_dots = len(dot_pics_with_dots)
        number_of_pics_with_blanks = len(dot_pics_with_blanks)
        number_of_small_boxes = number_of_pics_with_dots + number_of_pics_with_blanks
        self.assertEqual(number_of_small_boxes, 18)

        # James should see a continue message
        continue_message_on_feedback_page = self.browser.find_element_by_id(
            "go_to_prelim_two_again"
        ).text
        self.assertIn("Continue", continue_message_on_feedback_page)

        # James clicks on the continue message link
        continue_link_on_feedback_page = self.browser.find_element_by_id(
            "go_to_prelim_two_again"
        )
        continue_link_on_feedback_page.click()

        # James does the practise game again
        # He sees the countdown, then 3 by 3 grid
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-1'))
        )
        small_box_list = self.browser.find_elements_by_class_name(
            "col-sm-1"
        )
        number_of_small_boxes = len(small_box_list)
        self.assertEqual(number_of_small_boxes,9)

        # In the 3 by 3 grid there should be 3 dots
        dot_pics_with_dots = self.browser.find_elements_by_xpath('//img[@src="/static/doorgame/box_with_dot.png"]')
        number_of_dots = len(dot_pics_with_dots)
        self.assertEqual(number_of_dots,3)

        # James again cannot see a message displayed saying: "Can you remember the pattern from before?"
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

        # James remembers the pattern and then a blank grid appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'final_pattern_message'))
        )
        time.sleep(2)
        # Above the grid should be a message
        remember_pattern_message_actual = self.browser.find_element_by_id(
            "final_pattern_message"
        ).text
        self.assertIn(
            "Can you remember the pattern from before?",
            remember_pattern_message_actual
        )

        # James should see a message asking them to
        # continue to the next page
        time.sleep(2)
        link_to_feedback_second_go = self.browser.find_element_by_id(
            "play_again_link"
        )

        continue_message = link_to_feedback_second_go.get_attribute("value")
        self.assertIn("Continue to next page", continue_message)

        # James clicks on the link
        link_to_feedback_second_go.click()

        # James should see text saying, this is what you chose
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'feedback_text'))
        )
        feedback_text_message = self.browser.find_element_by_id(
            'feedback_text'
        ).text

        self.assertIn('This is what you chose:', feedback_text_message)

        # James should also see two nine by nine grids
        dot_pics_with_dots = self.browser.find_elements_by_xpath(
            '//img[@src="/static/doorgame/box_with_dot.png"]'
        )
        dot_pics_with_blanks = self.browser.find_elements_by_xpath(
            '//img[@src="/static/doorgame/box_empty.png"]'
        )
        number_of_pics_with_dots = len(dot_pics_with_dots)
        number_of_pics_with_blanks = len(dot_pics_with_blanks)
        number_of_small_boxes = number_of_pics_with_dots + number_of_pics_with_blanks
        self.assertEqual(number_of_small_boxes, 18)

        # James should see a continue message
        continue_message_on_feedback_page = self.browser.find_element_by_id(
            "go_to_prelim_four"
        ).text
        self.assertIn("Continue", continue_message_on_feedback_page)

        # James clicks on the continue message link
        continue_link_on_feedback_page = self.browser.find_element_by_id(
            "go_to_prelim_four"
        )
        continue_link_on_feedback_page.click()


        # James sees a well done message
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )

        well_done_message = self.browser.find_element_by_tag_name('h2').text
        self.assertIn("Well done", well_done_message)


        # James sees a continue message
        continue_message_on_prelim_four = self.browser.find_element_by_id(
            "go_to_prelim_five"
        ).text
        self.assertIn("Continue", continue_message_on_prelim_four)

        # James clicks on link
        continue_link_on_prelim_four = self.browser.find_element_by_id(
            "go_to_prelim_five"
        )
        continue_link_on_prelim_four.click()

        








