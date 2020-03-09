from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class BaseTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def login_temp(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')

