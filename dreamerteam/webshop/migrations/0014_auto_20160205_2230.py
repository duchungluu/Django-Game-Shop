# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webshop', '0013_auto_20160127_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=200, blank=True)),
                ('buy_started', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('buy_completed', models.DateTimeField(null=True)),
                ('buyer', models.ForeignKey(related_name='bought_games', to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(to='webshop.Game')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 2, 5)),
        ),
    ]
