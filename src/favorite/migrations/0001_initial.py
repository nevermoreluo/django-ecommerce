# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20160723_1351'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('favorite', models.ForeignKey(to='favorite.Favorite')),
                ('variation', models.ForeignKey(to='products.Variation')),
            ],
        ),
        migrations.AddField(
            model_name='favorite',
            name='items',
            field=models.ManyToManyField(to='products.Variation', through='favorite.FavoriteItem'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
