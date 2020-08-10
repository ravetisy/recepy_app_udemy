from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is needed to view/access the public endpoints"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()

        payload = {'email': 'testuser@gmail.com',
                   'password': 'testpass'
                   }
        self.user = create_user(**payload)
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test getting a list of ingredients"""

        Ingredient.objects.create(user=self.user, name='test_z')
        Ingredient.objects.create(user=self.user, name='test_a')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that only the ingredients for the
        authenticated user are returned"""

        payload = {'email': 'test2user@gmail.com',
                   'password': 'testpass'
                   }
        user2 = create_user(**payload)

        Ingredient.objects.create(user=user2, name='Test user 2')
        ingredient = Ingredient.objects.create(user=self.user, name='pamidor')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
