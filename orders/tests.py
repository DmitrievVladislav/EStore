from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from carts.models import Cart
from orders.views import OrderView
from products.models import Product
from users.models import User


class TestOrder(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('test_admin', '123456')
        self.product = Product.objects.create(
            title='test_p',
            price='40',
            description='test_d'
        )
        self.cart = Cart.objects.create(
            product_id=self.product.id,
            user_id=self.admin.id,
            quantity=11,
            price="12.00",
            total="132.00"
        )

    def test_order_create(self):
        factory = APIRequestFactory()
        request = factory.post('/orders/', {
            'address': 'test'},
                               format='json')
        force_authenticate(request, self.admin)
        order_view = OrderView.as_view()
        response = order_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        factory = APIRequestFactory()
        request = factory.get('/orders/')
        force_authenticate(request, self.admin)
        order_view = OrderView.as_view()
        response = order_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
