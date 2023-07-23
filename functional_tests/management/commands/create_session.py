from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    SESSION_KEY,
    get_user_model,
)
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

from functional_tests.test_data import test_login_data


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user_identifier')
        parser.add_argument('--size', default='three_by_three')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(
            options['user_identifier'],
            options['size']
        )
        self.stdout.write(session_key)

def create_pre_authenticated_session(user_identifier, size):
    # Retrieve name from dictionary
    user_details_one = test_login_data[user_identifier]
    username_one = user_details_one['username']
    password_one = user_details_one['password']

    user = User.objects.create_user(
        username=username_one,
        password=password_one
    )

    profile = user.profile
    if size == "three_by_three":
        profile.hard_or_easy_dots = "easy"
        profile.save()

    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
