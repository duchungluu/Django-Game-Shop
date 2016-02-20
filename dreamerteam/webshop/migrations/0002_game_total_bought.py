# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='total_bought',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
