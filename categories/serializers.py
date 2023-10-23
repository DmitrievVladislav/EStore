from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'parent_id',
            'picture',
            'background_color',
            'text_color'
        ]

class ShortCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
