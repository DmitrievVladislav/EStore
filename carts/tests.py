from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from .views import SingleCartUtils, CartView
from .models import Cart
from products.models import Product
from users.models import User


class TestCart(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('test_admin', '123456')
        self.product = Product.objects.create(
            title='test_p',
            price='40',
            description='test_d'
        )
        self.cart = Cart.objects.create(
            id=11,
            product_id=self.product.id,
            user_id=self.admin.id,
            quantity=11,
            price="12.00",
            total="132.00"
        )

    def test_cart_create(self):
        factory = APIRequestFactory()
        request = factory.post('/carts/', {
            'product': self.product.id,
            'quantity': 2},
                               format='json')
        force_authenticate(request, self.admin)
        cart_view = CartView.as_view()
        response = cart_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_carts(self):
        factory = APIRequestFactory()
        request = factory.get('/carts/')
        force_authenticate(request, self.admin)
        cart_view = CartView.as_view()
        response = cart_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart(self):
        factory = APIRequestFactory()
        request = factory.get(f'/carts/{self.cart.id}')
        force_authenticate(request, self.admin)
        cart_view = CartView.as_view()
        response = cart_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
