# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('favorite', '0004_auto_20160723_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
