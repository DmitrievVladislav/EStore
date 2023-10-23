import os
import xml.etree.ElementTree as ET

from categories.models import Category
from coreapp.settings import BASE_DIR
from offers.models import Offer
from products.models import Product, ProductParameter


class XMLParser:

    def get_data_from_xml(self):
        file_path = os.path.join(BASE_DIR, 'catalog.xml')
        tree = ET.parse(file_path)
        return tree.getroot()

    def get_category_dicts_list(self):
        root = self.get_data_from_xml()
        categories = []

        for category_elem in root.findall('.//category'):
            category = {
                'id': category_elem.get('id'),
                'title': category_elem.text,
                'parent_id': category_elem.get('parentId'),
                'picture': category_elem.get('picture'),
                'background_color': category_elem.get('backgroundColor'),
                'text_color': category_elem.get('textColor')
            }
            categories.append(category)
        return categories

    def get_offer_dicts_list(self):
        root = self.get_data_from_xml()
        offers = []

        for offer_elem in root.findall('.//offer'):
            offer = {
                'id': offer_elem.get('id'),
                'available': offer_elem.get('available'),
                'bid': offer_elem.get('bid'),
                'cbid': offer_elem.get('cbid'),
                'size_grid_image': offer_elem.get('sizeGridImage'),
                'added_on': offer_elem.get('addedOn'),
            }

            for element_name in ['group_id', 'price', 'old_price', 'vendor', 'vendorCode', 'modelVendorCode', 'model',
                                 'typePrefix', 'purchasable', 'delivery', 'useBonuses']:
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
            offer['cost'] = offer_elem.find('.//option').get('cost')
            offer['days'] = offer_elem.find('.//option').get('days')
            offers.append(offer)
        return offers

    def get_product_dicts_list(self):
        root = self.get_data_from_xml()
        products = []
        for product_elem in root.findall('.//offer'):
            product = {
                'available': product_elem.get('available'),
                'categoryIds': [category.text for category in product_elem.findall('categoryId')],
                'params': {}
            }

            for element_name in [
                'group_id', 'price', 'old_price', 'barcode', 'discount', 'description',
                'purchasable', 'preorder', 'url', 'model'
            ]:
                element = product_elem.find(element_name)
                product[element_name] = element.text if element is not None else None

            for param_elem in product_elem.findall('param'):
                name = param_elem.get('name')
                value = param_elem.text
                if name != 'Размер':
                    product['params'][name] = value

            products.append(product)
        return products

    def create_parameter(self, name, value, product_id):
        param = ProductParameter(
            product_id=product_id,
            name=name,
            value=value
        )
        param.save()

    def update_parameter(self, name, value, product_id):
        param = ProductParameter.objects.filter(product_id=product_id, name=name).first()
        param.value = value
        param.save()

    def create_product(self, product_dict):
        product = Product(
            id=product_dict['group_id'],
            default_available=bool(product_dict['available']),
            title=product_dict['model'],
            default_price=product_dict['price'],
            default_old_price=product_dict['old_price'],
            barcode=product_dict['barcode'],
            discount=product_dict['discount'],
            description=product_dict['description'],
            default_purchasable=bool(product_dict['purchasable']),
            preorder=bool(product_dict['preorder']),
            url=product_dict['url']
        )
        product.save()

        try:
            product.categories.set(product_dict['categoryIds'])
        except:
            pass

        if not ProductParameter.objects.filter(product_id=product.id).exists():
            for name, value in product_dict['params'].items():
                self.create_parameter(name, value, product_dict['group_id'])

    def create_offer(self, offer_dict):
        offer = Offer(
            id=offer_dict['id'],
            product_id=offer_dict['group_id'],
            available=bool(offer_dict['available']),
            bid=offer_dict['bid'],
            cbid=offer_dict['cbid'],
            size_grid_image=offer_dict['size_grid_image'],
            price=offer_dict['price'],
            old_price=offer_dict['old_price'],
            vendor=offer_dict['vendor'],
            vendor_code=offer_dict['vendorCode'],
            size=offer_dict['size'],
            purchasable=bool(offer_dict['purchasable']),
            delivery=bool(offer_dict['delivery']),
            use_bonuses=bool(offer_dict['useBonuses']),
            delivery_days=offer_dict['days'],
            delivery_cost=offer_dict['cost']
        )
        offer.save()

    def create_category(self, category_dict):
        category = Category(**category_dict)
        category.save()

    def update_category(self, category, category_dict):
        for key, value in category_dict.items():
            setattr(category, key, value)
        category.save()

    def update_product(self, product, product_dict):
        product.id = product_dict['group_id']
        product.default_available = bool(product_dict['available'])
        product.title = product_dict['model']
        product.default_price = product_dict['price']
        product.default_old_price = product_dict['old_price']
        product.barcode = product_dict['barcode']
        product.discount = product_dict['discount']
        product.description = product_dict['description']
        product.default_purchasable = bool(product_dict['purchasable'])
        product.preorder = bool(product_dict['preorder'])
        product.url = product_dict['url']
        product.save()

        try:
            product.categories.set(product_dict['categoryIds'])
        except:
            pass

        for name, value in product_dict['params'].items():
            if ProductParameter.objects.filter(product_id=product.id, name=name).exists():
                self.update_parameter(name, value, product_dict['group_id'])

    def update_offer(self, offer, offer_dict):
        offer.product_id = offer_dict['group_id']
        offer.available = bool(offer_dict['available'])
        offer.bid = offer_dict['bid']
        offer.cbid = offer_dict['cbid']
        offer.size_grid_image = offer_dict['size_grid_image']
        offer.price = offer_dict['price']
        offer.old_price = offer_dict['old_price']
        offer.vendor = offer_dict['vendor']
        offer.vendor_code = offer_dict['vendorCode']
        offer.size = offer_dict['size']
        offer.purchasable = bool(offer_dict['purchasable'])
        offer.delivery = bool(offer_dict['delivery'])
        offer.use_bonuses = bool(offer_dict['useBonuses'])
        offer.delivery_days = offer_dict['days']
        offer.delivery_cost = offer_dict['cost']
        offer.save()

    def add_xml_categories_in_db(self):
        categories = self.get_category_dicts_list()

        for category_dict in categories:
            category = Category.objects.filter(id=category_dict['id']).first()
            if category:
                self.update_category(category, category_dict)
            else:
                self.create_category(category_dict)

    def add_xml_offers_in_db(self):
        offers = self.get_offer_dicts_list()

        for offer_dict in offers:
            offer = Offer.objects.filter(id=offer_dict['id']).first()
            if offer:
                self.update_offer(offer, offer_dict)
            else:
                self.create_offer(offer_dict)

    def add_xml_products_in_db(self):
        products = self.get_product_dicts_list()

        for product_dict in products:
            product = Product.objects.filter(id=product_dict['group_id']).first()
            if product:
                self.update_product(product, product_dict)
            else:
                self.create_product(product_dict)

    def add_xml_in_db(self):
        self.add_xml_categories_in_db()
        self.add_xml_products_in_db()
        self.add_xml_offers_in_db()
