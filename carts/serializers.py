from rest_framework import serializers

from carts.models import Cart, Promocode


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'offer', 'user', 'quantity', 'price', 'old_total', 'total']


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ['id', 'promocode', 'discount']


class PostCartCalcSerializer(serializers.Serializer):
    promocode = serializers.CharField()
    discount = serializers.IntegerField()
    bonus = serializers.IntegerField()
    is_delivery = serializers.BooleanField()
