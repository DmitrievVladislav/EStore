# Generated by Django 4.2.6 on 2023-10-23 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_productparameter_parameter_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='purchasable',
            new_name='default_purchasable',
        ),
    ]
