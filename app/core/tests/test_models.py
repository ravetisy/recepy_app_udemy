from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='testrecepyapp@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'testrecepyapp@gmail.com'
        password = 'TestPassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normilized(self):
        """Test the email for the new user is normalized"""
        email = 'testrecepyapp@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'TestPassword123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a enw superuser"""
        user = get_user_model().objects.create_superuser(
            'testsuperuser@gmail.com',
            'admin'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_string(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
