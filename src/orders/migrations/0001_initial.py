# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=120, choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created')),
                ('shipping_total_price', models.DecimalField(decimal_places=2, max_digits=50, default=5.99)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=50)),
                ('order_id', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=120, choices=[('billing', 'Billing'), ('shipping', 'Shipping')])),
                ('street', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('zipcode', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='UserCheckout',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('braintree_id', models.CharField(max_length=120, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(to='orders.UserCheckout'),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(to='orders.UserAddress', null=True, related_name='billing_address'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(to='cart.Cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(to='orders.UserAddress', null=True, related_name='shipping_address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, to='orders.UserCheckout'),
        ),
    ]
