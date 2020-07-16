import unittest
from django.test import Client
from django.core.urlresolvers import reverse
from centr_osvita.users.factories import UserFactory
from centr_osvita.profiles.factories import ProfileFactory


class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.url = reverse('users:login')
        self.client = Client()

        self.user = UserFactory()
        self.profile = ProfileFactory(user=self.user)

        self.good_login_data = {
            "username": self.user.phone,
            "password": '12345678',
        }
        self.bad_login_data = {
            "username": self.user.phone,
            "password": '1234567',
        }

    def test_login_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(self.url, self.good_login_data, follow=True)
        self.assertEqual(('/', 302) in response.redirect_chain, True)
        self.assertEqual(response.status_code, 200)

    def test_login_failed(self):
        response = self.client.post(self.url, self.bad_login_data)
        self.assertEqual('<ul class="errorlist nonfield">' in str(response.content), True)
        self.assertEqual(response.status_code, 200)
