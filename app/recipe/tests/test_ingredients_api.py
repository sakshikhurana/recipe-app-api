from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer


INGREDIENT_URLS = reverse('recipe:ingredient-list')


class PublicIngredientAPITests(TestCase):
    """Test the publicallly available ingredient API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URLS)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Test the privately available ingredient API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.com',
                                                           'testpass')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENT_URLS)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that only ingredients for authenticated users are retrieved"""
        user2 = get_user_model().objects.create_user('test1@gmail.com',
                                                     'testpass')
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Turmeric')
        res = self.client.get(INGREDIENT_URLS)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredients(self):
        """Test create a new ingredient"""
        payload = {'name':'Cabbage'}
        self.client.post(INGREDIENT_URLS, payload)
        exists = Ingredient.objects.filter(user=self.user, 
                                           name=payload['name'])
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredients fails"""
        payload = {'name':''}
        res = self.client.post(INGREDIENT_URLS, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipe(self):
        """Test filtering ingredients by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(user=self.user, name='Apples')
        ingredient2 = Ingredient.objects.create(user=self.user, name='Chicken')
        recipe = Recipe.objects.create(title='Apple Pie', time_minutes=50,
                                       price=15.00, user=self.user)
        recipe.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENT_URLS, {'assigned_only': 1})
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        