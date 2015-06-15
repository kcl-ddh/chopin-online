# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocve', '0005_update_ocve_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accode',
            options={'ordering': ['accode'], 'verbose_name': 'AcCode', 'verbose_name_plural': 'AcCodes'},
        ),
    ]
