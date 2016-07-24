# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_sale_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('variation', models.OneToOneField(to='products.Variation')),
            ],
        ),
    ]
