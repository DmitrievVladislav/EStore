from django.db import models

from products.models import Product
from users.models import User


class Offer(models.Model):
    product_id = models.IntegerField()
    available = models.BooleanField(default=False)
    bid = models.IntegerField()
    cbid = models.IntegerField()
    size_grid_image = models.TextField(default=None, null=True)
    added_on = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    old_price = models.DecimalField(max_digits=20, decimal_places=2, default=None)
    vendor = models.CharField(max_length=255)
    vendorCode = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = 'offerss'
        ordering = ('id',)
