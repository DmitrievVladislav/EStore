from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductsSerializer


class ProductsView(APIView):

    def get_sorted_by_price_products(self, min, max):
        products = Product.objects.filter(price__range=(min, max)).order_by('price').values()
        serialized_products = ProductsSerializer(products, many=True)
        return serialized_products.data

    def check_conditions(self, min, max):
        if min is None and max is None:
            products = Product.objects.all().order_by('id').all()
            serialized_products = ProductsSerializer(products, many=True)
            return serialized_products.data
        elif min is not None and max is not None:
            return self.get_sorted_by_price_products(min, max)
        elif min is None:
            return self.get_sorted_by_price_products(0, max)
        elif max is None:
            return self.get_sorted_by_price_products(min, 999999)


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
    @permission_classes([IsAdminUser])
    def get(self, request):
        min = request.query_params.get("min")
        max = request.query_params.get("max")
        return Response(self.check_conditions(min, max))

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
    def post(self, request):
        serialized_product = ProductsSerializer(data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialized_product.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUtils(APIView):

    @swagger_auto_schema(
        operation_summary="Получить выбранный товар",
        responses={
            200: ProductsSerializer(many=True),
            500: "Серверная ошибка"},
    )
    @permission_classes(AllowAny)
    def get(self, request, id):
        products = Product.objects.filter(id=id).first()
        serializer = ProductsSerializer(products)
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
    def put(self, request, id):
        product = Product.objects.filter(id=id).first()
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

# @api_view(['GET'])
# def get_product(request, id):
#     product = Product.objects.filter(id=id).first()
#     serializer = ProductsSerializer(product)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_products(request):
#     products = Product.objects.all()
#     serializer = ProductsSerializer(products, many=True)
#     return Response(serializer.data)

#         category_id = 2
# product_id = Product.objects.filter(
#     title=request.data.get("title"),
#     description=request.data.get("description"),
#     price=request.data.get("price")
# ).first().id
# Category.objects.filter(id=category_id).first().products.add(product_id)