from django.db import models

from products.models import Product
from users.models import User


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    purchasable = models.BooleanField(default=True)
    bid = models.IntegerField()
    cbid = models.IntegerField()
    size_grid_image = models.TextField(default=None, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True)
    vendor = models.CharField(max_length=255, null=True)
    vendor_code = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    discount = models.IntegerField(default=0)
    delivery = models.BooleanField(default=False)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_days = models.IntegerField(default=0)
    use_bonuses = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'offers'
        ordering = ('id',)
