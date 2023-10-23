from rest_framework.serializers import ModelSerializer

from .models import Product, RecentlyViewed, ProductParameter


class ParamsSerializer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['name', 'value']


class ProductsSerializer(ModelSerializer):
    parameters = ParamsSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class RecentlyViewedSerializer(ModelSerializer):
    class Meta:
        model = RecentlyViewed
        fields = ['id', 'user_id', 'product_id', 'viewed_at']
