from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from doorgame.views import home_page, door_result_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = home_page(request)  
        html = response.content.decode('utf8')  
        #self.assertTrue(html.startswith('<html>'))  
        self.assertIn('<h2>Welcome to the door game</h2>', html)  
        #self.assertTrue(html.endswith('</html>'))

class DoorResultPageTest(TestCase):

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_page_returns_correct_html(self):
        pass