from django.db import migrations

import hashlib


def copy_users(apps, schema_editor):
    """Copies user information from the Django User model to the OCVEUser
    model."""
    User = apps.get_model('auth', 'User')
    OCVEUser = apps.get_model('ocve', 'OCVEUser')
    for user in User.objects.all():
        ocve_user = OCVEUser()
        ocve_user.id = user.id
        ocve_user.username = user.username
        ocve_user.save()

def delete_users(apps, schema_editor):
    """Deletes all the OCVEUser objects."""
    OCVEUser = apps.get_model('ocve', 'OCVEUser')
    OCVEUser.objects.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ocve',
         '0004_auto_20150526_1619'),
    ]

    operations = [
        migrations.RunPython(copy_users, reverse_code=delete_users)
    ]
