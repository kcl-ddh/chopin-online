# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocve', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accode',
            name='accode_hash',
            field=models.CharField(default='', max_length=256, editable=False),
            preserve_default=False,
        ),
    ]
