from django.db import migrations
from django.db.models import Q

import random

SEPARATOR = ':::'


def invalidate_duplicate_ac_codes(apps, schema_editor):
    """Invalidates the AC code by adding a prefix to the duplicate AC codes
    that are not linked to SourceInformation objects."""
    AcCode = apps.get_model('ocve', 'AcCode')
    Source = apps.get_model('ocve', 'Source')

    for ac in AcCode.objects.all():
        if not Source.objects.filter(sourceinformation__accode=ac).filter(
            Q(ocve=1) | Q(cfeo=1)):
            ac.accode = str(random.uniform(0, 9)) + SEPARATOR + ac.accode
            ac.save()


def restore_duplicate_ac_codes(apps, schema_editor):
    """Removes the duplicate prefix from the AC codes."""
    AcCode = apps.get_model('ocve', 'AcCode')
    for ac in AcCode.objects.filter(accode__contains=SEPARATOR):
        ac.accode = ac.accode.split(SEPARATOR)[1]
        ac.save()


class Migration(migrations.Migration):
    dependencies = [('ocve', '0006_auto_20150615_1037'), ]
    operations = [
        migrations.RunPython(invalidate_duplicate_ac_codes,
                             reverse_code=restore_duplicate_ac_codes)
    ]
