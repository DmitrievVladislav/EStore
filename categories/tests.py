from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from .views import Category, CategoriesView
from products.models import Product
from users.models import User

class TestMPTT(TestCase):

    def test_hierarchy(self):
        root = Category.objects.create(title="Root")
        clothes = Category.objects.create(title="Одежда", parent=root)
        woman_clothes = Category.objects.create(title="Женская одежда", parent=clothes)
        tshirts = Category.objects.create(title="Рубашки", parent=woman_clothes)
        assert root.get_descendants()

class TestCategory(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('test_admin', '123456')
        self.ca = Category.objects.create(
            title='test_c',
            parent=None
        )

    def test_get_categories(self):
        factory = APIRequestFactory()
        request = factory.get('/carts/')
        force_authenticate(request, self.admin)
        categories = CategoriesView.as_view()
        response = categories(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)