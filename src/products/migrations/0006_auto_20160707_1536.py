# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(max_digits=20, default=2, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variation',
            name='sale_price',
            field=models.DecimalField(max_digits=20, default='1', decimal_places=2),
            preserve_default=False,
        ),
    ]
