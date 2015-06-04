# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ocve.models_generic


class Migration(migrations.Migration):

    dependencies = [
        ('ocve', '0003_generate_accode_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCVEUser',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=256)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='user',
            field=models.ForeignKey(default=1, to='ocve.OCVEUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='barcollection',
            name='user_id',
            field=models.IntegerField(default=-1, verbose_name=ocve.models_generic.OCVEUser),
            preserve_default=True,
        ),
    ]
