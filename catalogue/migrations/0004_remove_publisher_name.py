# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_publisher_name_to_rich_text_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='name',
        ),
    ]
