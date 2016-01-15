# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0008_remove_game_developers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='games',
            field=models.ManyToManyField(to='webshop.Game', related_name='developers'),
        ),
    ]
