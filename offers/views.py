from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers.models import Offer
from .serializers import OfferSerializer


class OfferView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить все офферы",
        responses={
            200: OfferSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        offers = Offer.objects.all()
        x = XMLParser()
        x.add_xml_in_db()
        if not offers:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)


class ProductOfferView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить офферы по id товара",
        responses={
            200: OfferSerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request, product_id):
        offers = Offer.objects.filter(product=product_id)
        if not offers:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
