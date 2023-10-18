from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET

from categories.models import Category
from categories.serializers import CategorySerializer


class XMLParser():

    def get_data_from_xml(self):
        tree = ET.parse('C:\\Users\\Inform\\PycharmProjects\\coreapp\\test.xml')
        root = tree.getroot()
        return root

    def get_category_model(self):
        tree = ET.parse('C:\\Users\\Inform\\PycharmProjects\\coreapp\\test.xml')
        root = tree.getroot()
        print(root.tag)
        for elem in root:
            category_title = elem.text
            category_id = elem.get('id')
            category_parent_id = elem.get('parentId', None)
            category_picture = elem.get('picture', None)
            category_background_color = elem.get('backgroundColor', None)
            category_text_color = elem.get('textColor', None)
            category = Category.objects.filter(id=category_id).first()
            parent_category = Category.objects.filter(id=category_parent_id).first()
            if category:
                category.title = category_title
                category.id = category_id
                category.parent = parent_category
                category.picture = category_picture
                category.background_color = category_background_color
                category.text_color = category_text_color
                category.save()
            else:
                category = Category(
                    title=category_title,
                    id=category_id,
                    parent=parent_category,
                    picture=category_picture,
                    background_color=category_background_color,
                    text_color=category_text_color
                )
                category.save()


class OfferView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="test",
        responses={
            200: CategorySerializer(many=True),
            500: "Серверная ошибка"},
    )
    def get(self, request):
        xmlp = XMLParser()
        xmlp.get_data_from_xml()
        xmlp.get_category_model()
        return Response(status=status.HTTP_200_OK)

# Create your views here.
# print('Title:', elem.text)
# print('ID:', elem.get('id', None))
# print('parentId:', elem.get('parentId', None))
# print('picture:', elem.get('picture', None))
# print('backgroundColor:', elem.get('backgroundColor', None))
# print('textColor:', elem.get('textColor', None))
