from rest_framework import serializers

from carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'user_id', 'quantity', 'price', 'total']


class PostCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']