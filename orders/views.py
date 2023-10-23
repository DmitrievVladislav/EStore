from dadata import Dadata
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.models import Cart
from orders.models import Order
from orders.serializers import OrderSerializer

api_key = "502c427e4efb9091b78ae5c71c5e27370c49a801"
secret_key = "bdaaa53d260bc678154cec4f456cecfaeec41aa4"
dadata = Dadata(api_key, secret_key)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение списка всех заказов юзера",
        responses={
            200: OrderSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        if not orders:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def get_correct_adress(self, address):
        adrs = dadata.clean(name="address", source=address)
        return adrs['result']

    def fill_order(self, order, carts):
        for cart in carts:
            order.total_quantity += cart.quantity
            order.offers.add(cart.offer)
            order.total_sum = cart.all_user_carts_total
        order.save()
        return

    @swagger_auto_schema(
        operation_summary="Создание заказа",
        request_body=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: "Неправильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    @csrf_exempt
    def post(self, request):
        carts = Cart.objects.filter(user_id=request.user.id)
        if not carts:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order = Order(user_id=request.user.id)
        order.address = self.get_correct_adress(request.data.get("address"))
        order.save()
        self.fill_order(order, carts)
        carts.delete()
        return Response(status=status.HTTP_201_CREATED)
