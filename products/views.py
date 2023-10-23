from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, RecentlyViewed
from .serializers import ProductsSerializer


class ProductsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить список всех товаров",
        manual_parameters=[
            openapi.Parameter('min', openapi.IN_QUERY, description="Минимальная цена",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('max', openapi.IN_QUERY, description="Максимальная цена",
                              type=openapi.TYPE_INTEGER)],
        responses={
            200: ProductsSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        min_value = request.query_params.get("min")
        max_value = request.query_params.get("max") or 99999
        if min_value is None:
            min_value = 0

        products = Product.objects.prefetch_related('categories').filter(
            default_price__range=(min_value, max_value)).order_by('default_price')
        if not products:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)


class EditSingleProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Измененить выбранный товар",
        responses={
            202: "Изменения приняты",
            400: "Неправильный ввод данных",
            500: "Серверная ошибка",
        },
        request_body=ProductsSerializer
    )
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удалить выбранный товар",
        responses={
            204: ProductsSerializer(many=True),
            500: "Серверная ошибка"
        }
    )
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddSingleProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Добавить товар",
        request_body=ProductsSerializer,
        responses={
            201: ProductsSerializer,
            400: "Неправильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    @csrf_exempt
    def post(self, request):
        serialized_product = ProductsSerializer(data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialized_product.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleProductView(APIView):
    permission_classes = [AllowAny]

    def add_viewed_product(self, user, product):
        try:
            viewed_products = RecentlyViewed.objects.get(user_id=user.id, product_id=product.id)
        except RecentlyViewed.DoesNotExist:
            viewed_products = RecentlyViewed(
                user=user,
                product=product
            )
        viewed_products.save()

    @swagger_auto_schema(
        operation_summary="Получить выбранный товар",
        responses={
            200: ProductsSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        self.add_viewed_product(request.user, product)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)


class RecommendedProductsView(APIView):
    permission_classes = [IsAuthenticated]
    last_viewed_length = 5

    @swagger_auto_schema(
        operation_summary="Получить последние просмотренные товары",
        responses={
            200: ProductsSerializer(many=True),
            404: "Не найдено",
            500: "Ошибка сервера"}
    )
    def get(self, request):
        if not request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        products = Product.objects.filter(recentlyviewed__user_id=request.user.id).order_by(
            '-recentlyviewed__viewed_at')
        if not products:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(products, many=True)
        last_product = serializer.data[self.last_viewed_length - 1]['id']
        last_viewed = RecentlyViewed.objects.filter(product_id=last_product, user_id=request.user.id).delete()
        viewed_on_del = RecentlyViewed.objects.filter(viewed_at__lt=last_viewed)
        if viewed_on_del.exists():
            for v_elem in viewed_on_del:
                v_elem.delete()
        return Response(serializer.data)
