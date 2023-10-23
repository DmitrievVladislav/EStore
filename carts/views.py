from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.models import Cart, Promocode
from carts.serializers import CartSerializer, PromocodeSerializer, PostCartCalcSerializer
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
        carts = Cart.objects.select_related('offer', 'user').filter(user_id=request.user.id)
        if not carts:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(carts, many=True)
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
        if not (offer.available or offer.purchasable):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart = Cart.objects.select_related('offer', 'user').filter(offer_id=offer_id, user_id=request.user.id).first()
        if not cart:
            cart = Cart(
                offer_id=offer.id,
                quantity=quantity,
                user_id=request.user.id,
                price=offer.price,
                total=offer.price * quantity
            )
            cart.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleCartView(APIView):
    permission_classes = [IsAuthenticated]

    def change_total_status(self, user_id, total):
        carts = Cart.objects.select_related('offer', 'user').filter(user_id=user_id)
        if not carts:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for cart in carts:
            cart.all_user_carts_total = total
            cart.save()

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
    @csrf_exempt
    def put(self, request, cart_id):
        quantity = request.data.get("quantity")
        cart = get_object_or_404(Cart, id=cart_id, user_id=request.user.id)
        if quantity <= 0:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        cart.quantity = quantity
        cart.total = cart.price * quantity
        cart.old_total = 0
        cart.all_user_carts_total = 0
        cart.save()
        # self.change_total_status(request.user.id, cart.all_user_carts_total)
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


class CartCalculationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Пересчитать стоимость корзины с учетом скидок",
        request_body=PostCartCalcSerializer,
        responses={
            201: CartSerializer,
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    @csrf_exempt
    def post(self, request):
        input_promocode = request.data.get("promocode")
        bonus = request.data.get("bonus")
        promocode = Promocode.objects.filter(promocode=input_promocode).first()
        max_delivery_cost = 0
        carts = Cart.objects.select_related('offer', 'user').filter(user_id=request.user.id)
        if not carts:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not promocode:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for cart in carts:
            if cart.offer.delivery_cost > max_delivery_cost:
                max_delivery_cost = cart.offer.delivery_cost
            temp_discount = cart.offer.discount + promocode.discount
            if temp_discount >= 99:
                temp_discount = 99
            cart.old_total = cart.price * cart.quantity
            cart.total = ((100 - float(temp_discount)) / 100) * float(cart.old_total)
            cart.save()
        carts_total = carts.aggregate(total=Sum('total'))
        for cart in carts:
            cart.all_user_carts_total = carts_total['total']
            if request.data.get('is_delivery'):
                cart.all_user_carts_total += max_delivery_cost
            if 0 < bonus <= cart.all_user_carts_total:
                cart.all_user_carts_total -= bonus
            cart.save()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)


class PromocodesView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Добавить промокод",
        request_body=PromocodeSerializer,
        responses={
            201: PromocodeSerializer,
            400: "Неверные данные",
            404: "Не найдено",
            500: "Ошибка сервера",
        },
    )
    @csrf_exempt
    def post(self, request):
        input_prom = request.data.get("promocode")
        discount = request.data.get("discount")
        if discount <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        promocode = Promocode.objects.filter(promocode=input_prom).first()
        if not promocode:
            promocode = Promocode(
                promocode=input_prom,
                discount=discount
            )
            promocode.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Получить список промокодов",
        responses={
            200: PromocodeSerializer(many=True),
            404: "Не найдено",
            500: "Ошибка сервера"},
    )
    def get(self, request):
        promocodes = Promocode.objects.all()
        if not promocodes:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PromocodeSerializer(promocodes, many=True)
        return Response(serializer.data)
