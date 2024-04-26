from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import UserModel


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Valid registration data
    def test_registration_success(self):
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'supersecret',
        }
        response = self.client.post('/signup', valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the user was created
        self.assertTrue("username" in response.data)
        self.assertEqual(response.data["username"], valid_data["username"])

    # Invalid registration data (validate email field)
    def test_registration_invalid_email(self):
        invalid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe.example.com',
            'password': 'supersecret',
        }
        response = self.client.post('/signup', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the expected error message is returned
        expected_error = {
            "email": ["Enter a valid email address."],
        }
        self.assertEqual(response.data, expected_error)

    # Invalid registration data (missing required field 'first_name, last_name, password')
    def test_registration_required_data(self):
        invalid_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
        }
        response = self.client.post('/signup', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the expected error message is returned
        expected_error = {
            "first_name": ["This field is required."],
            "last_name": ["This field is required."],
            "password": ["This field is required."]
        }
        self.assertEqual(response.data, expected_error)


class LogInTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(first_name='John', last_name='Doe', username='johndoe', email='johndoe@example.com', password='supersecret')

    # Valid login data
    def test_login_success(self):
        valid_data = {
            'email': 'johndoe@example.com',
            'password': 'supersecret',
        }
        response = self.client.post('/login', valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the expected UID is returned in the response
        self.assertTrue("UID" in response.data)
        self.assertEqual(response.data["UID"], self.user.id)

    # Invalid login data
    def test_login_invalid_password(self):
        invalid_data = {
            'email': 'johndoe@example.com',
            'password': 'Supersecret',
        }
        response = self.client.post('/login', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Check if the expected error message is returned
        expected_error = {
            'Error': 'Incorrect email or password'
        }
        self.assertEqual(response.data, expected_error)

    # Missing login data (email)
    def test_login_missing_credentials(self):
        missing_data = {
            'password': 'password'
        }
        response = self.client.post('/login', missing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the expected error message is returned
        expected_error = {
            'email': ['This field is required.']
        }
        self.assertEqual(response.data, expected_error)
