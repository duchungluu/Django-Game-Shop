# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('webshop', '0003_developer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='group_ptr',
        ),
        migrations.AddField(
            model_name='game',
            name='developers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
    ]
