from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=510)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created',)

