from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET

from categories.models import Category
from categories.serializers import CategorySerializer
from .models import Offer


class XMLParser:

    def get_data_from_xml(self):
        tree = ET.parse('C:\\Users\\Inform\\PycharmProjects\\coreapp\\test.xml')
        return tree.getroot()

    def get_category_dicts_list(self):
        root = self.get_data_from_xml()
        categories = []
        for category_elem in root.findall('.//category'):
            category = dict()
            category['id'] = category_elem.get('id')
            category['title'] = category_elem.text
            category['parent_id'] = category_elem.get('parentId', None)
            category['picture'] = category_elem.get('picture', None)
            category['background_color'] = category_elem.get('backgroundColor', None)
            category['text_color'] = category_elem.get('textColor', None)
            categories.append(category)
        return categories

    def get_offer_dicts_list(self):
        root = self.get_data_from_xml()
        offers = []
        for offer_elem in root.findall('.//offer'):
            offer = {}
            offer_id = offer_elem.get('id')
            offer['id'] = offer_id
            offer['available'] = offer_elem.get('available')
            offer['bid'] = offer_elem.get('bid')
            offer['cbid'] = offer_elem.get('cbid')
            offer['size_grid_image'] = offer_elem.get('sizeGridImage', None)
            offer['added_on'] = offer_elem.get('addedOn')
            for element_name in ['group_id', 'price', 'old_price', 'vendor', 'vendorCode', 'modelVendorCode', 'model',
                                 'typePrefix']:
                element = offer_elem.find(element_name)
                if element is not None:
                    offer[element_name] = element.text
                else:
                    offer[element_name] = None
            for param_elem in offer_elem.findall('param'):
                param_name = param_elem.get('name')
                param_unit = param_elem.get('unit')
                if param_name == "Размер" and param_unit == "RU":
                    offer['size'] = param_elem.text
            offers.append(offer)
        return offers

    def create_offer(self, offer_dict):
        offer = Offer(
            id=offer_dict['id'],
            product_id=offer_dict['group_id'],
            available=bool(offer_dict['available']),
            bid=offer_dict['bid'],
            cbid=offer_dict['cbid'],
            size_grid_image=offer_dict['size_grid_image'],
            added_on=offer_dict['added_on'],
            price=offer_dict['price'],
            old_price=offer_dict['old_price'],
            vendor=offer_dict['vendor'],
            vendor_code=offer_dict['vendorCode'],
            size=offer_dict['size']
        )
        offer.save()

    def create_category(self, parent_category, category_dict):
        category = Category(
            title=category_dict['title'],
            id=category_dict['id'],
            parent=parent_category,
            picture=category_dict['picture'],
            background_color=category_dict['background_color'],
            text_color=category_dict['text_color']
        )
        category.save()

    def update_category(self, category, parent_category, category_dict):
        category.title = category_dict['title']
        category.id = category_dict['id']
        category.parent = parent_category
        category.picture = category_dict['picture']
        category.background_color = category_dict['background_color']
        category.text_color = category_dict['text_color']
        category.save()

    def update_offer(self, offer, offer_dict):
        offer.available = bool(offer_dict['available'])
        offer.bid = offer_dict['bid']
        offer.cbid = offer_dict['cbid']
        offer.size_grid_image = offer_dict['size_grid_image']
        offer.added_on = offer_dict['added_on']
        offer.price = offer_dict['price']
        offer.old_price = offer_dict['old_price']
        offer.vendor = offer_dict['vendor']
        offer.vendor_code = offer_dict['vendorCode']
        offer.size = offer_dict['size']
        offer.save()

    def add_xml_categories_in_db(self):
        categories = self.get_category_dicts_list()
        for category_dict in categories:
            category = Category.objects.filter(id=category_dict['id']).first()
            parent_category = Category.objects.filter(id=category_dict['parent_id']).first()
            if category:
                self.update_category(category, parent_category, category_dict)
            else:
                self.create_category(parent_category, category_dict)

    def add_xml_offers_in_db(self):
        offers = self.get_offer_dicts_list()
        for offer_dict in offers:
            offer = Offer.objects.filter(id=offer_dict['id']).first()
            if offer:
                self.update_offer(offer, offer_dict)
            else:
                self.create_offer(offer_dict)


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
        xmlp.add_xml_categories_in_db()
        xmlp.add_xml_offers_in_db()
        return Response(status=status.HTTP_200_OK)
