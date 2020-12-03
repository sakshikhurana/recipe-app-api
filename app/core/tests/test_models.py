from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def test_create_user_with_email_successful(self):
        """Test the user is created with email successfully"""
        email = 'test@gmail.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user email is normalized"""
        email = 'test@GMAIL.COM'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test invalid email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')

    def test_create_superuser_with_email_successful(self):
        """Test the user is created with email successfully"""
        email = 'test@gmail.com'
        password = 'password123'
        user = get_user_model().objects.create_superuser(
            email=email, password=password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
