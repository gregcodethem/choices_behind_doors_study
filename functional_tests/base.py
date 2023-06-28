import time

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from doorgame.models import Profile

test_login_data = {
    "John": {"username": "johndoe", "password": "bigfisharetasty3"},
    "Ozen": {"username": "ozen", "password": "Russia432"},
    "Bob": {"username": "bob", "password": "bobbob123"},
}

# A helper function to get the profile for a specific username
def get_profile_by_username(username):
    try:
        # Retrieve the User instance by username
        user = User.objects.get(username=username)

        # Access the associated Profile instance
        profile = user.profile

        return profile

    except User.DoesNotExist:
        print(f"User with username {username} does not exist.")
        return None


class BaseTest(LiveServerTestCase):

    def create_user(
            self,
            user_identifier="John",
            size="three_by_three",
    ):
        # retrieve name from dictionary
        user_details_one = test_login_data[user_identifier]
        username_one = user_details_one['username']
        password_one = user_details_one['password']

        self.user = User.objects.create_user(
            username=username_one,
            password=password_one
        )
        profile = get_profile_by_username(username_one)
        if size=="three_by_three":
            profile.hard_or_easy_dots = "easy"
            profile.save()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.create_user()

    def tearDown(self):
        self.browser.quit()

    def login(self, user_identifier="John"):
        # Enter username and password
        time.sleep(1)
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
        time.sleep(3)
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
        self.assertIn('You chose ' + door_number, chosen_message)
