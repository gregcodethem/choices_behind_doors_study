import time
import os

from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from doorgame.models import Profile
from .server_tools import (
    create_session_on_server,
    reset_database
)
from .management.commands.create_session import create_pre_authenticated_session
from .test_data import test_login_data
from env_host import USERNAME_ON_HOST


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


class attribute_has_changed(object):
  def __init__(self, locator, attribute, old_value):
    self.locator = locator
    self.attribute = attribute
    self.old_value = old_value

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    new_value = element.get_attribute(self.attribute)
    if new_value != self.old_value:
        return element
    else:
        return False

class BaseTest(LiveServerTestCase):

    def create_pre_authenticated_session(self, user_identifier, size):
        if self.staging_server:
            session_key = create_session_on_server(
                self.staging_server,
                user_identifier,
                size
            )
        else:
            session_key = create_pre_authenticated_session(user_identifier, size)
        self.browser.get(self.live_server_url + '/404_no_such_url')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )
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
        print('users at start of setUp in base.py:')
        print([user.username for user in User.objects.all()])
        print([user.password for user in User.objects.all()])
        print('end of list')
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(USERNAME_ON_HOST, self.staging_server)

        self.create_user()
        print('setUp ran, now sleeping for 3 seconds')
        print('users at end of setUp in base.py:')
        print([user.username for user in User.objects.all()])
        print([user.password for user in User.objects.all()])
        print('end of list')
        time.sleep(1)

    def tearDown(self):
        self.browser.quit()

    def login(self, user_identifier="John"):
        # Enter username and password
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input_box = self.browser.find_element(
            By.ID,
            'id_username'
        )
        user_login_info = test_login_data[user_identifier]
        username = user_login_info["username"]
        password = user_login_info["password"]
        username_input_box.send_keys(
            username)
        password_input_box = self.browser.find_element(
            By.ID,
            'id_password'
        )
        password_input_box.send_keys(password)

        # click Login
        password_input_box.send_keys(Keys.ENTER)

    def user_goes_straight_to_first_door_game_via_memory_game(
            self,
            user_identifier="John"
    ):
        if user_identifier is not "John":
            self.create_user(user_identifier=user_identifier)
        # James accesses website and logs in
        self.browser.get(self.live_server_url)
        # Login screen appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        # James logs in
        self.login(user_identifier=user_identifier)
        time.sleep(0.5)

        # James has completed all the prelims and sees memory game
        # James sees countdown, then 3 by 3 grid

        first_real_memory_game_url = self.live_server_url + '/memory_game_initial_turn'
        self.browser.get(first_real_memory_game_url)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-1'))
        )

        # James is automatically redirected to the door game
        time.sleep(2)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'door1'))
        )


    def logout(self):
        logout_url = self.live_server_url + '/accounts/logout'
        self.browser.get(logout_url)
        # Login screen appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )


    def user_clicks_through_memory_game(self):
        memory_title = self.browser.find_element(By.TAG_NAME,'h2').text

        # user can go to door game
        go_to_door_game = self.browser.find_element(By.ID, 'go_to_door_game')
        go_to_door_game.click()
        time.sleep(1)

    def user_chooses_a_door(self, door_number):
        # door_number must be string of format 'door1' etc

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, door_number))
        )

        door_to_choose = self.browser.find_element(By.ID, door_number)
        # user clicks on door1
        door_to_choose.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'result_of_first_door_choice'))
        )
