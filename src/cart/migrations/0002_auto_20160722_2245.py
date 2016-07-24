# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(max_digits=50, default=0.0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(max_digits=50, default=0.0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(max_digits=50, default=0.0, decimal_places=2),
        ),
    ]
