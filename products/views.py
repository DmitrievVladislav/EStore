from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, RecentlyViewed
from .serializers import ProductsSerializer


class ProductsView(APIView):

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
    @permission_classes(IsAdminUser)
    def get(self, request):
        min_value = request.query_params.get("min")
        max_value = request.query_params.get("max")
        if min_value is None:
            min_value = 0
        if max_value is None:
            max_value = 999999
        products = Product.objects.filter(default_price__range=(min_value, max_value)).order_by('default_price')
        if not products:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Добавить товар",
        request_body=ProductsSerializer,
        responses={
            201: ProductsSerializer,
            400: "Неправильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    @permission_classes(IsAdminUser)
    @csrf_exempt
    def post(self, request):
        serialized_product = ProductsSerializer(data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialized_product.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleProductView(APIView):
    @swagger_auto_schema(
        operation_summary="Получить выбранный товар",
        responses={
            200: ProductsSerializer(many=True),
            500: "Серверная ошибка"},
    )
    @permission_classes(AllowAny)
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        try:
            viewed_products = RecentlyViewed.objects.get(user_id=request.user.id, product_id=product.id)
        except RecentlyViewed.DoesNotExist:
            viewed_products = RecentlyViewed(
                user=request.user,
                product=product
            )
        viewed_products.save()
        serializer = ProductsSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Измененить выбранный товар",
        responses={
            202: "Изменения приняты",
            400: "Неправильный ввод данных",
            500: "Серверная ошибка",
        },
        request_body=ProductsSerializer
    )
    @permission_classes(IsAdminUser)
    def put(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
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
    @permission_classes(IsAdminUser)
    def delete(self, request, id):
        product = Product.objects.filter(id=id).first()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendedProductsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить последние просмотренные товары",
        responses={
            200: ProductsSerializer(many=True),
            404: "Не найдено",
            500: "Ошибка сервера"},
    )
    def get(self, request):
        products = Product.objects.filter(recentlyviewed__user_id=request.user.id).order_by(
            '-recentlyviewed__viewed_at')[1:6]
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
