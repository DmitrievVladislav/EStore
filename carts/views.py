from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from carts.models import Cart
from carts.serializers import CartSerializer, PostCartSerializer
from products.models import Product


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить список товаров в корзине",
        responses={
            200: CartSerializer(many=True),
            404: "Не найдено",
            500: "Ошибка сервера"},
    )
    def get(self, request):
        cart = Cart.objects.filter(user_id=request.user.id).values()
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Добавить товар в корзину",
        request_body=PostCartSerializer,
        responses={
            201: PostCartSerializer,
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    def post(self, request):
        product = Product.objects.filter(id=request.data.get("product")).first()
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        quantity = request.data.get("quantity")
        if quantity <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart = Cart(
            product=product,
            quantity=quantity,
            user=request.user,
            price=product.price)
        cart.total = cart.total_sum()
        cart.save()
        return Response(status=status.HTTP_201_CREATED)


class SingleCartUtils(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_object(self, cart_id, user_id):
        return Cart.objects.filter(id=cart_id, user_id=user_id).first()

    @swagger_auto_schema(
        operation_summary="Изменение единицы товара в корзине",
        request_body=PostCartSerializer,
        responses={
            201: CartSerializer,
            204: "Данные удалены",
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },

    )
    def put(self, request, cart_id):
        cart = self.get_cart_object(cart_id, request.user.id)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if cart.quantity <= 0:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CartSerializer(cart, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(
        operation_summary="Удаление товара из корзины",
        responses={
            201: CartSerializer,
            204: "Данные удалены",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    def delete(self, request, cart_id):
        cart = self.get_cart_object(cart_id, request.user.id)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Получение информации о конкретном товаре в корзине",
        responses={
            201: CartSerializer,
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    def get(self, request, cart_id):
        cart = self.get_cart_object(cart_id, request.user.id)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # @swagger_auto_schema(
    #     operation_summary="Изменение товара из корзине",
    #     request_body=PostCartSerializer,
    #     responses={
    #         201: PostCartSerializer,
    #         204: "Данные удалены",
    #         404: "Не найдено",
    #         500: "Ошибка сервера",
    #     },
    # )
    # def post(self, request, cart_id):
    #     cart = self.get_cart_object(cart_id, request.user.id)
    #     if not cart:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     cart.quantity = request.data.get("quantity")
    #     if cart.quantity <= 0:
    #         cart.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     cart.total = cart.total_sum()
    #     cart.save()
    #     return Response(status=status.HTTP_201_CREATED)