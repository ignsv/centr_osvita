import unittest
from django.test import Client
from django.core.urlresolvers import reverse
from centr_osvita.users.models import User
from centr_osvita.profiles.models import Profile


class UserRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.url = reverse('users:register')
        self.client = Client()
        User.objects.all().delete()
        Profile.objects.all().delete()

        self.good_sign_up_data = {
            'phone': '+380970000001',
            'password': '12345678',
            'full_name': 'John Doe Jr.',
            'parent_full_name': 'John Doe',
            'parent_phone': '+380980000001',
            'institution_name': 'Oxford',
            'grade': '9'
        }
        self.bad_sign_up_data = {
            'phone': '+38097000',
            'password': '12345678',
            'full_name': 'John Doe Jr.',
            'parent_full_name': 'John Doe',
            'parent_phone': '+380980000001',
            'institution_name': 'Oxford',
            'grade': '9'
        }

    def test_sign_up_success(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        response = self.client.post(self.url, self.good_sign_up_data, follow=True)
        self.assertEqual(('/', 302) in response.redirect_chain, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_sign_up_failed(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        response = self.client.post(self.url, self.bad_sign_up_data)
        self.assertEqual('<ul class="errorlist">' in str(response.content), True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
