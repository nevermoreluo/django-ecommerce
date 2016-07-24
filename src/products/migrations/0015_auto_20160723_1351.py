# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_favoriteitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriteitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='favoriteitem',
            name='variation',
        ),
        migrations.DeleteModel(
            name='FavoriteItem',
        ),
    ]
