# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
# from rest_framework import status

# from accounts.serializers import SignUpSerializer

# User = get_user_model()


# class SignUpSerializerTest(TestCase):
#     def test_signup_serializer_valid_data(self):
#         data = {
#             'username': 'test_user',
#             'email': 'test@example.com',
#             'password': 'test_password',
#             'confirm_password': 'test_password'
#         }
#         serializer = SignUpSerializer(data=data)
#         self.assertTrue(serializer.is_valid())

#     def test_signup_serializer_password_mismatch(self):
#         data = {
#             'username': 'test_user',
#             'email': 'test@example.com',
#             'password': 'test_password',
#             'confirm_password': 'mismatch_password'
#         }
#         serializer = SignUpSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('non_field_errors', serializer.errors)

#     def test_signup_serializer_existing_email(self):
#         User.objects.create_user(
#             username='existing_user', email='test@example.com', password='existing_password')
#         data = {
#             'username': 'test_user',
#             'email': 'test@example.com',
#             'password': 'test_password',
#             'confirm_password': 'test_password'
#         }
#         serializer = SignUpSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('email', serializer.errors)


# class SignUpAPIViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_signup_api_view(self):
#         url = '/api/v1/accounts/signup/'
#         data = {
#             'username': 'test_user',
#             'email': 'test@example.com',
#             'password': 'test_password',
#             'confirm_password': 'test_password'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('access', response.data)
#         self.assertIn('refresh', response.data)

#     def test_signup_api_view_existing_email(self):
#         User.objects.create_user(
#             username='existing_user', email='test@example.com', password='existing_password')
#         url = '/api/v1/accounts/signup/'
#         data = {
#             'username': 'test_user',
#             'email': 'test@example.com',
#             'password': 'test_password',
#             'confirm_password': 'test_password'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
