# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20160708_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_to),
        ),
        migrations.AlterField(
            model_name='variation',
            name='inventory',
            field=models.IntegerField(null=True, default='0', blank=True),
        ),
    ]
