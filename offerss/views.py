from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OfferSerializer
from .models import Offer


class OfferView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="test",
        responses={
            200: OfferSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        offfers = Offer.objects.all()
        serializer = OfferSerializer(offfers, many=True)
        return Response(serializer.data)

    def post(self, request):

        return Response()
