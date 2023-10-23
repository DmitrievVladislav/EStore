from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
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
        if not categories:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
        category_products = Product.objects.filter(categories=category_id).prefetch_related('categories')
        if not category_products:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
        if not categories:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data)
