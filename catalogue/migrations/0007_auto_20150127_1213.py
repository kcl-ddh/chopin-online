# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_landingpage_landingpagesection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='landingpage',
            options={},
        ),
        migrations.AddField(
            model_name='landingpagesection',
            name='css_class',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
