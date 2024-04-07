from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import CustomUser


class SignUpAPIViewTest(TestCase):
    def test_signup_api_view(self):
        url = reverse('signup')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


class VerifyAPIViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', password='testpassword')

    def test_verify_api_view(self):
        self.client.force_login(self.user)
        url = reverse('verify')
        data = {'code': '12345'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', password='testpassword')

    def test_login_api_view(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Authentication status updated successfully')


