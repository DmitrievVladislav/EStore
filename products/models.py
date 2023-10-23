from django.db import models

from users.models import User
from categories.models import Category


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    default_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    default_old_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=False, default=None)
    discount = models.IntegerField(default=None, null=True, blank=True)
    default_available = models.BooleanField(default=False)
    description = models.TextField(default=None, null=True)
    default_purchasable = models.BooleanField(default=True)
    preorder = models.BooleanField(default=False)
    url = models.TextField(default=None, null=True)
    categories = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created',)


class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-viewed_at',)


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Другой вариант параметров
# class Parameter(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
#
# class ProductParameter(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
#     value = models.CharField(max_length=255)

