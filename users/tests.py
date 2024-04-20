from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .serializers import RegistrationSerializer, LogInSerializer


# Create your tests here.
UserModel = get_user_model()

class RegistrationSerializerTestCase(TestCase):
    def test_valid_registration_data(self):
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'supersecret',
        }
        serializer = RegistrationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_create_user(self):
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'supersecret',
        }
        serializer = RegistrationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, UserModel)
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')
        # Add more assertions as needed

    def test_invalid_registration_data(self):
        invalid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalidemail',  # Invalid email format
            'password': 'short',       # Password too short
        }
        serializer = RegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        # Check specific fields for errors
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)


class LogInSerializerTestCase(TestCase):
    def test_valid_login_data(self):
        user = UserModel.objects.create_user(username='johndoe', email='johndoe@example.com', password='supersecret')
        login_data = {
            'email': 'johndoe@example.com',
            'password': 'supersecret',
        }
        serializer = LogInSerializer(data=login_data)
        self.assertTrue(serializer.is_valid())
        # Check if email and password are in validated_data
        self.assertIn('email', serializer.validated_data)
        self.assertIn('password', serializer.validated_data)

    def test_invalid_login_data(self):
        user = UserModel.objects.create_user(username='johndoe', email='johndoe@example.com', password='supersecret')
        invalid_login_data = {
            'email': 'johndoe@example.com',
            'password': 'wrongpassword',  # Incorrect password
        }
        serializer = LogInSerializer(data=invalid_login_data)
        self.assertFalse(serializer.is_valid())
        # Check if serializer raises ValidationError
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
