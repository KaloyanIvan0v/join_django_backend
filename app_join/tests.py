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

task = {
    "title": "Test Task",
    "description": "This is a test task.",
    "state": "To Do",
    "prio": "High",
    "dueDate": "2024-12-31",
    "category": "Testing"
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

    def test_get_task_authorized(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.post('/api/v1/tasks/', task, format='json')
        self.assertEqual(response.status_code, 201)

    def test_delete_task(self):
        response = self.client.post('/api/v1/tasks/', task, format='json')
        task_id = response.data['id']
        delete_response = self.client.delete(f'/api/v1/tasks/{task_id}/')
        self.assertEqual(delete_response.status_code, 204)
