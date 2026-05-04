from django.test import TestCase
from rest_framework.test import APIClient


user0 = {
    "display_name": "testuser",
    "email": "testy@mail.de",
    "password": "testpass123",
    "repeated_password": "testpass123"
}

user1 = {
    "display_name": "testuser1",
    "email": "testy1@mail.de",
    "password": "testpass123",
    "repeated_password": "testpass123"
}


class RegistrationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.post('/api/v1/auth/register/', user0, format='json')

    def test_register_valid_data(self):
        response = self.client.post(
            '/api/v1/auth/register/', user1, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_email_already_exists(self):
        response = self.client.post(
            '/api/v1/auth/register/', user0, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)


class LoginTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.post('/api/v1/auth/register/', user0, format='json')

    def test_login_valid_credentials(self):
        response = self.client.post('/api/v1/auth/login/', {
            'email': user0['email'],
            'password': user0['password']
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/v1/auth/login/', {
            'email': user0['email'],
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
