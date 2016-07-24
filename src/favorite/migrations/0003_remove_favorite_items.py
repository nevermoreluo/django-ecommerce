# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorite', '0002_auto_20160723_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='items',
        ),
    ]
