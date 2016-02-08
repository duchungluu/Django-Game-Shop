# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webshop', '0017_auto_20160208_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={},
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(default=2, related_name='developed_games', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
