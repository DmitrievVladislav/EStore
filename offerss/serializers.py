from rest_framework.serializers import ModelSerializer

from .models import Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'id',
            'product_id',
            'available',
            'bid',
            'cbid',
            'size_grid_image',
            'added_on',
            'price',
            'old_price',
            'vendor',
            'vendor_code',
            'size',
        ]
