# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160706_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('sale_price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(blank=True, null=True, default='-1')),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
    ]
