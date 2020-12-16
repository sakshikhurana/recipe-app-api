from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='testpass'):
    """Create sample user"""
    return get_user_model().objects.create_user(email,password)

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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name='Vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test that ingredient string representation"""
        ingredient = models.Ingredient.objects.create(user=sample_user(), 
                                                      name='Cucumber')
        self.assertEqual(str(ingredient), ingredient.name)
