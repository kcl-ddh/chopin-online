# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_landingpage_landingpagesection'),
    ]

    operations = [
        migrations.AddField(
            model_name='impression',
            name='ocve_ac_code',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
