from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers import ProductsSerializer
from .models import Category
from .serializers import CategorySerializer


class CategoriesView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить список категорий",
        responses={
            200: CategorySerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductsCategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить товары принадлежащие категории",
        responses={
            200: ProductsSerializer(many=True),
            500: "Серверная ошибка"}
    )
    def get(self, request, category_id):
        category_products = Category.objects.filter(id=category_id).first().related_products
        serialized_categories = ProductsSerializer(category_products, many=True)
        return Response(serialized_categories.data)

class SingleCategoryDetails(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить дочерние элементы категории",
        responses={
            200: CategorySerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request, category_id):
        categories = Category.objects.filter(id=category_id).first().get_descendants()
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data)

# def get_category_object(id):
#     return Category.objects.filter(id=id).first()
#
# @swagger_auto_schema(
#     method='GET',
#     operation_summary="Получить список категорий",
#     responses={
#         200: CategorySerializer(many=True),
#         500: "Серверная ошибка"},
# )
# @api_view(['GET'])
# def get_categories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)
#
# @swagger_auto_schema(
#     method='GET',
#     operation_summary="Получить одну категорию",
#     responses={
#         200: CategorySerializer(),
#         500: "Серверная ошибка"},
# )
# @api_view(['GET'])
# def get_category(request, id):
#     category = get_category_object(id)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)
#
# @swagger_auto_schema(
#     method='GET',
#     operation_summary="Получить товары принадлежащие категории",
#     responses={
#         200: ProductsSerializer(many=True),
#         500: "Серверная ошибка"},
# )
# @api_view(['GET'])
# def get_category_products(request, id):
#     products_in_category = get_category_object(id).related_products
#     serializer = ProductsSerializer(products_in_category, many=True)
#     return Response(serializer.data)