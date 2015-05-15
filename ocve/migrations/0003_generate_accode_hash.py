from django.db import migrations

import hashlib


def load_accode_hash(apps, schema_editor):
    """Saves all the AcCode objects to generate the accode hash for each one of
    them."""
    AcCode = apps.get_model('ocve', 'AcCode')
    for ac in AcCode.objects.all():
        ac.accode_hash = hashlib.md5(ac.accode.encode('UTF-8')).hexdigest()
        ac.save()

def unload_accode_hash(apps, schema_editor):
    """Removes all the accode hash from the AcCode objects."""

    AcCode = apps.get_model('ocve', 'AcCode')
    for ac in AcCode.objects.all():
        ac.accode_hash = ''
        ac.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ocve',
         '0002_accode_accode_hash'),
    ]

    operations = [
        migrations.RunPython(load_accode_hash,
                             reverse_code=unload_accode_hash),
    ]
