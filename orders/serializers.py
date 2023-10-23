from rest_framework import serializers

from offers.serializers import OfferSerializer
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'offers', 'user', 'address', 'total_sum', 'total_quantity', 'status', 'created']
