# Generated by Django 3.2.15 on 2022-08-11 16:43

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_product_memory_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=api.models.get_img_upload_path),
        ),
    ]
