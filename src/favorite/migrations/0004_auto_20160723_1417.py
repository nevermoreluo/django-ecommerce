# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20160723_1351'),
        ('favorite', '0003_remove_favorite_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoriteitem',
            old_name='item',
            new_name='variation',
        ),
        migrations.AddField(
            model_name='favorite',
            name='favoriteItem',
            field=models.ManyToManyField(to='products.Variation', through='favorite.FavoriteItem'),
        ),
    ]
