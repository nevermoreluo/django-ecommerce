# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20160708_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
        migrations.AlterField(
            model_name='variation',
            name='sale_price',
            field=models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True),
        ),
    ]
