# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocve', '0007_remove_duplicate_ac_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accode',
            name='accode',
            field=models.CharField(default=b'', unique=True, max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
