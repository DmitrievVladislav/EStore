from rest_framework.serializers import ModelSerializer

from .models import Product, RecentlyViewed


class ProductsSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class RecentlyViewedSerializer(ModelSerializer):
    class Meta:
        model = RecentlyViewed
        fields = ['id', 'user_id', 'product_id', 'viewed_at']
