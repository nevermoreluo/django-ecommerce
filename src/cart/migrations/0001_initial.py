# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_productfeatured'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('subtotal', models.DecimalField(default=25.0, decimal_places=2, max_digits=50)),
                ('tax_percentage', models.DecimalField(default=0.085, decimal_places=5, max_digits=10)),
                ('tax_total', models.DecimalField(default=25.0, decimal_places=2, max_digits=50)),
                ('total', models.DecimalField(default=25.0, decimal_places=2, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_item_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(to='cart.Cart')),
                ('item', models.ForeignKey(to='products.Variation')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='products.Variation', through='cart.CartItem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
