# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0004_auto_20160115_1950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'permissions': (('buy_game', 'Can buy games'),)},
        ),
    ]
