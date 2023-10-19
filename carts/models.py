from django.db import models

from products.models import Product
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='u_carts', on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, related_name='p_carts', blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def total_sum(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = 'carts'
        ordering = ('-created',)

class Promocode(models.Model):
    promocode = models.CharField(max_length=255)
    discount = models.IntegerField()