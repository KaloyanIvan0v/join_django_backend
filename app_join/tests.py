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


class TaskTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        access = self.client.post(
            '/api/v1/auth/register/', user0, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

    def test_get_task_unauthorized(self):
        self.clientUnauth = APIClient()
        response = self.clientUnauth.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 401)
