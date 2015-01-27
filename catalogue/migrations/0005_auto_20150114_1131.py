# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_remove_publisher_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publisher',
            old_name='name_rich_text',
            new_name='name',
        ),
    ]
