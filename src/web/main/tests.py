from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class DarkNetTests(TestCase):

    def test_auth_protection(self):
        unauth_client = Client()
        response = unauth_client.get(reverse('darknet'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/darknet/')


class SessionsTests(TestCase):

    def test_auth_protection(self):
        unauth_client = Client()
        response = unauth_client.get(reverse('sessions'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
