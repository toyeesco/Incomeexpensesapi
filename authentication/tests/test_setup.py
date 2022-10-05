from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import  Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),
            'username': self.fake.username().split('@')[0],
            'password': self.fake.email(),
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
