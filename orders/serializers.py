from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'products', 'user_id', 'address', 'total_sum', 'total_quantity', 'status',  'created']
