from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from .views import ProductsView
from .models import Product
from users.models import User


class TestCart(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('test_admin', '123456')
        self.product = Product.objects.create(
            title='test_p',
            price='40',
            description='test_d'
        )


    def test_get_products(self):
        factory = APIRequestFactory()
        request = factory.get('/carts/')
        force_authenticate(request, self.admin)
        products = ProductsView.as_view()
        response = products(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

