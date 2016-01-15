# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('webshop', '0002_auto_20160106_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('group_ptr', models.OneToOneField(serialize=False, to='auth.Group', parent_link=True, primary_key=True, auto_created=True)),
                ('ourownname', models.CharField(max_length=50)),
            ],
            bases=('auth.group',),
        ),
    ]
