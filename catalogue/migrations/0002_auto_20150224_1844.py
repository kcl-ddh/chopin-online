# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='rubric',
            field=wagtail.wagtailcore.fields.RichTextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stp',
            name='rubric',
            field=wagtail.wagtailcore.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
