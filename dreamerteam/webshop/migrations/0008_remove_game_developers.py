# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0007_auto_20160115_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='developers',
        ),
    ]
