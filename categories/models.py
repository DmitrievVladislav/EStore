from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from products.models import Product


class Category(MPTTModel):
    title = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    picture = models.TextField(default=None)
    background_color = models.CharField(max_length=255)
    text_color = models.CharField(max_length=255)
    related_products = models.ManyToManyField(Product, blank=True, db_constraint=False)

    def __str__(self):
        return self.title

    class MPTTMeta:
        verbose_name_plural = 'categories'
        order_insertion_by = ['title']
# Create your models here.
