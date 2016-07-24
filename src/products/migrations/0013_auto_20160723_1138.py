# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_favoriteitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteitem',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
