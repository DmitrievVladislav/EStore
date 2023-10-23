from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from carts.models import Cart
from carts.serializers import CartSerializer
from offers.models import Offer


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
        cart = Cart.objects.filter(user_id=request.user.id)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Добавить товар в корзину",
        request_body=CartSerializer,
        responses={
            201: CartSerializer,
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    @csrf_exempt
    def post(self, request):
        quantity = request.data.get("quantity")
        offer_id = request.data.get("offer")
        if quantity <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        offer = get_object_or_404(Offer, id=offer_id)  # Проверка на доступность + извлечение цены
        if not offer.available:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart = Cart.objects.filter(offer_id=offer_id, user=request.user).first()
        if not cart:
            cart = Cart(
                offer_id=offer.id,
                quantity=quantity,
                user=request.user,
                price=offer.price,
                total=offer.price * quantity
            )
            cart.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleCartUtils(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Изменение единицы товара в корзине",
        request_body=CartSerializer,
        responses={
            201: CartSerializer,
            204: "Данные удалены",
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    def put(self, request, cart_id):
        quantity = request.data.get("quantity")
        cart = get_object_or_404(Cart, id=cart_id, user_id=request.user.id)
        if quantity <= 0:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        cart.quantity = quantity
        cart.total = cart.price * quantity
        cart.save()
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
        cart = get_object_or_404(Cart, id=cart_id, user_id=request.user.id)
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
        cart = get_object_or_404(Cart, id=cart_id, user_id=request.user.id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
