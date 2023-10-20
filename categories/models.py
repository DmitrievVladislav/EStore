from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class Category(MPTTModel):
    title = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    picture = models.TextField(default=None, null=True)
    background_color = models.CharField(max_length=255, default=None, null=True)
    text_color = models.CharField(max_length=255, default=None, null=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        verbose_name_plural = 'categories'
        order_insertion_by = ['id']
# Create your models here.
