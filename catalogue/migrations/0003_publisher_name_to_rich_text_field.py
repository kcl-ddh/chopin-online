# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.contrib.wagtailroutablepage.models
import django.utils.timezone
import wagtail.wagtailcore.fields
import model_utils.fields


def copy_publisher_name(apps, schema_editor):
    Publisher = apps.get_model('catalogue', 'Publisher')

    for p in Publisher.objects.all():
        if p.name:
            p.name_rich_text = p.name
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20150114_1117'),
    ]

    operations = [
        migrations.RunPython(copy_publisher_name),
    ]
