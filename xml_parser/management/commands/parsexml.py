from django.core.management.base import BaseCommand
from xml_parser.xml_parser import XMLParser


class Command(BaseCommand):
    help = 'Выполнить парсинг Categories и Offers из XML файла'

    def handle(self, *args, **options):
        xmlp = XMLParser()
        try:
            xmlp.add_xml_in_db()
            self.stdout.write(self.style.SUCCESS('Parsed successfully!'))
        except:
            self.stdout.write(self.style.ERROR('Parsing error'))
