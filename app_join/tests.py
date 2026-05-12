from django.test import TestCase
from rest_framework.test import APIClient
from app_join.models import Task, Contact
from app_join import test_data


class TaskTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        access = self.client.post(
            '/api/v1/auth/register/', test_data.user0, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        self.client.post('/api/v1/contacts/', test_data.contact, format='json')

    def test_get_task_unauthorized(self):
        self.clientUnauth = APIClient()
        response = self.clientUnauth.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 401)

    def test_get_task_authorized(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.task, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_single_task(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.task, format='json')
        task_id = response.data['id']
        get_response = self.client.get(f'/api/v1/tasks/{task_id}/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.data['title'], test_data.task['title'])

    def test_get_not_existing_task(self):
        response = self.client.get('/api/v1/tasks/9999/')
        self.assertEqual(response.status_code, 404)

    def test_patch_task(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.task, format='json')
        task_id = response.data['id']
        patch_response = self.client.patch(
            f'/api/v1/tasks/{task_id}/', test_data.taskPatch, format='json')
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(
            patch_response.data['title'], test_data.taskPatch['title'])

    def test_create_task_invalid_data(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.taskInvalid, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.task, format='json')
        task_id = response.data['id']
        delete_response = self.client.delete(f'/api/v1/tasks/{task_id}/')
        self.assertEqual(delete_response.status_code, 204)

    def test_create_task_with_not_existing_contact(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.taskWithNotExistingContact, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

    def test_add_not_existing_contact_to_task(self):
        response = self.client.post(
            '/api/v1/tasks/', test_data.task, format='json')
        task_id = response.data['id']
        update_response = self.client.put(
            f'/api/v1/tasks/{task_id}/', test_data.taskWithNotExistingContact, format='json')
        self.assertEqual(update_response.status_code, 400)
        task = Task.objects.get(id=task_id)
        self.assertEqual(task.assignedTo.count(), 0)


class ContactTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        access = self.client.post(
            '/api/v1/auth/register/', test_data.user0, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

    def test_get_contacts_unauthorized(self):
        unauth = APIClient()
        response = unauth.get('/api/v1/contacts/')
        self.assertEqual(response.status_code, 401)

    def test_get_contacts_authorized(self):
        response = self.client.get('/api/v1/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_create_contact(self):
        response = self.client.post(
            '/api/v1/contacts/', test_data.contact, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 1)

    def test_get_single_contact(self):
        contact_id = self.client.post(
            '/api/v1/contacts/', test_data.contact, format='json').data['id']
        response = self.client.get(f'/api/v1/contacts/{contact_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], test_data.contact['email'])

    def test_update_contact(self):
        contact_id = self.client.post(
            '/api/v1/contacts/', test_data.contact, format='json').data['id']
        response = self.client.put(
            f'/api/v1/contacts/{contact_id}/', test_data.contactUpdate, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],
                         test_data.contactUpdate['name'])

    def test_delete_contact(self):
        contact_id = self.client.post(
            '/api/v1/contacts/', test_data.contact, format='json').data['id']
        response = self.client.delete(f'/api/v1/contacts/{contact_id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contact.objects.count(), 0)

    def test_get_not_existing_contact(self):
        response = self.client.get('/api/v1/contacts/9999/')
        self.assertEqual(response.status_code, 404)
