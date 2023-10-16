from rest_framework.serializers import ModelSerializer

from .models import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'created',
            'is_superuser',
            'is_staff',
            'password'
        ]

