# Generated by Django 4.2.6 on 2023-10-20 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recentlyviewed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='categories.category'),
        ),
    ]
