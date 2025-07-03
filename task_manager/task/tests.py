from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from task.models import Task  
class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.register_url = '/api/register/'  
        self.login_url = '/api/login/' 
        self.task_url = '/api/tasks/'

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()

        # Obtain JWT token
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
        print(response)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_registration(self):
        data = {'username': 'newuser', 'password': 'newpass123'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_task(self):
        data = {'title': 'Test Task', 'description': 'Test Description'}
        response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_get_tasks(self):
        Task.objects.create(user=self.user, title='Task 1', description='Desc 1')
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_update_task(self):
        task = Task.objects.create(user=self.user, title='Task 1', description='Desc 1')
        url = reverse('task_detail', kwargs={'pk': task.pk})
        response = self.client.put(url, {'completed': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, title='Task 1', description='Desc 1')
        url = reverse('task_detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    