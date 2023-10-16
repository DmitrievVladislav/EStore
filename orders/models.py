from django.db import models

from products.models import Product
from users.models import User

class Order(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    address = models.TextField(default='Воронеж', null=True)
    total_sum = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=256, default='В обработке')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'orders'
        ordering = ('-created',)

