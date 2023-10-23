from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UsersSerializer


class UsersView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Получить список всех пользователей",
        responses={
            200: UsersSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)



