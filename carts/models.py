from django.db import models

from offers.models import Offer
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    offer = models.ForeignKey(Offer, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    old_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_discounted = models.BooleanField(default=False)
    delivery_days = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'carts'
        ordering = ('-created',)


class Promocode(models.Model):
    promocode = models.CharField(max_length=255)
    discount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'promocodes'
