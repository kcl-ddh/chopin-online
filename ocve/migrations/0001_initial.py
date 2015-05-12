# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accode', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'AcCode',
                'verbose_name_plural': 'AcCodes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notetext', models.TextField(default=b'', blank=True)),
                ('noteregions', models.TextField(default=b'', blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Annotation',
                'verbose_name_plural': 'Annotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Annotation_BarRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annotation', models.ForeignKey(to='ocve.Annotation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnnotationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annotationType', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default=b'', blank=True)),
                ('siglum', models.CharField(default=b'', max_length=255, blank=True)),
                ('notes', models.TextField(default=b'', blank=True)),
            ],
            options={
                'verbose_name': 'Archive',
                'verbose_name_plural': 'Archives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barnumber', models.IntegerField(null=True, blank=True)),
                ('barlabel', models.TextField(default=b'', blank=True)),
            ],
            options={
                'verbose_name': 'Bar',
                'verbose_name_plural': 'Bars',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar_BarRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bar', models.ForeignKey(default=1, to='ocve.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BarCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(default=-1, verbose_name=django.contrib.auth.models.User)),
                ('name', models.TextField(default=b'', blank=True)),
                ('xystring', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BarRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField(null=True, blank=True)),
                ('y', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('anomaly', models.IntegerField(default=0, blank=True)),
                ('barid_old', models.IntegerField(null=True, blank=True)),
                ('annotation', models.ManyToManyField(to='ocve.Annotation', null=True, through='ocve.Annotation_BarRegion', blank=True)),
                ('bar', models.ManyToManyField(to='ocve.Bar', null=True, through='ocve.Bar_BarRegion', blank=True)),
            ],
            options={
                'verbose_name': 'BarRegion',
                'verbose_name_plural': 'BarRegions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BarSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('endbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BarSpine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('orderNo', models.IntegerField(default=0, null=True, blank=True)),
                ('implied', models.IntegerField(default=0, null=True, blank=True)),
                ('bar', models.ForeignKey(default=1, to='ocve.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'CollectionType',
                'verbose_name_plural': 'CollectionTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(default=b'', max_length=255, blank=True)),
                ('countryabbrev', models.CharField(default=b'', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dedicatee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dedicatee', models.TextField(default=b'', blank=True)),
                ('alternateOf', models.ForeignKey(related_name='alternate', default=1, to='ocve.Dedicatee')),
            ],
            options={
                'ordering': ['dedicatee'],
                'verbose_name': 'Dedicatee',
                'verbose_name_plural': 'Dedicatees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EditStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'NONE', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.CharField(default=b'', max_length=255, blank=True)),
                ('pluralname', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre_Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.ForeignKey(to='ocve.Genre')),
            ],
            options={
                'ordering': ['work'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument', models.CharField(default=b'', max_length=255, blank=True)),
                ('instrumentabbrev', models.CharField(default=b'', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'Instrument',
                'verbose_name_plural': 'Instruments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='instrumentComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument', models.ForeignKey(default=1, to='ocve.Instrument')),
            ],
            options={
                'verbose_name': 'instrumentComponent',
                'verbose_name_plural': 'instrumentComponents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='keyMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keymode', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'keyMode',
                'verbose_name_plural': 'keyModes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='keyPitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keypitch', models.CharField(default=b'', max_length=255, blank=True)),
                ('orderno', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['orderno'],
                'verbose_name': 'keyPitch',
                'verbose_name_plural': 'keyPitches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewPageImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surrogate', models.IntegerField(null=True, blank=True)),
                ('versionnumber', models.IntegerField(null=True, blank=True)),
                ('permission', models.BooleanField(default=False)),
                ('permissionnote', models.CharField(default=b'', max_length=255, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('filename', models.CharField(default=b'', max_length=255, blank=True)),
                ('startbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('endbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('corrected', models.IntegerField(default=0, null=True, blank=True)),
                ('linked', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'NewPageImage',
                'verbose_name_plural': 'NewPageImages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('library', models.TextField(default=b'', blank=True)),
                ('copyright', models.TextField(default=b'', blank=True)),
                ('sourcecode', models.CharField(default=b'', max_length=255, blank=True)),
                ('sourcecreated', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewSourceInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locationsimilarcopies', models.TextField(default=b'', blank=True)),
                ('reprints', models.TextField(default=b'', blank=True)),
                ('seriestitle', models.CharField(default=b'', max_length=255, blank=True)),
                ('copyright', models.CharField(default=b'', max_length=255, blank=True)),
                ('contentssummary', models.CharField(default=b'', max_length=255, blank=True)),
                ('contents', models.TextField(default=b'', help_text='Edition text', blank=True)),
                ('shelfmark', models.CharField(default=b'', max_length=255, blank=True)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('datepublication', models.CharField(default=b'', max_length=255, blank=True)),
                ('leaves', models.IntegerField(null=True, blank=True)),
                ('sourcecode', models.CharField(default=b'', max_length=255, blank=True)),
                ('title', models.TextField(default=b'', blank=True)),
                ('publicationtitle', models.TextField(default=b'', blank=True)),
                ('imagesource', models.CharField(default=b'', max_length=255, blank=True)),
                ('platenumber', models.CharField(default=b'', max_length=255, blank=True)),
                ('additionalInformation', models.TextField(default=b'', blank=True)),
                ('keyFeatures', models.TextField(default=b'', blank=True)),
                ('volume', models.CharField(default=b'', max_length=255, blank=True)),
                ('accode', models.ForeignKey(default=1, to='ocve.AcCode')),
                ('archive', models.ForeignKey(default=1, to='ocve.Archive')),
                ('dedicatee', models.ForeignKey(default=1, to='ocve.Dedicatee')),
            ],
            options={
                'verbose_name': 'SourceInformation',
                'verbose_name_plural': 'SourceInformations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Opus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opusno', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Opus',
                'verbose_name_plural': 'Opuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('orderno', models.IntegerField(null=True, blank=True)),
                ('preferredversion', models.IntegerField(default=1, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surrogate', models.IntegerField(null=True, blank=True)),
                ('textlabel', models.TextField(default=b'', blank=True)),
                ('versionnumber', models.IntegerField(null=True, blank=True)),
                ('permission', models.BooleanField(default=False)),
                ('permissionnote', models.CharField(default=b'', max_length=255, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('startbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('endbar', models.CharField(default=b'', max_length=255, blank=True)),
                ('corrected', models.IntegerField(null=True, blank=True)),
                ('page', models.ForeignKey(default=1, to='ocve.Page')),
            ],
            options={
                'verbose_name': 'PageImage',
                'verbose_name_plural': 'PageImages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageLegacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ocveKey', models.IntegerField(null=True, blank=True)),
                ('cfeoKey', models.IntegerField(null=True, blank=True)),
                ('filename', models.TextField(default=b'', blank=True)),
                ('storageStructure', models.TextField(default=b'', blank=True)),
                ('cropCorrected', models.IntegerField(default=0, null=True, blank=True)),
                ('jp2', models.CharField(default=b'UNVERIFIED', max_length=255, blank=True)),
                ('editstatus', models.ForeignKey(default=1, to='ocve.EditStatus')),
                ('pageimage', models.ForeignKey(default=1, to='ocve.PageImage')),
            ],
            options={
                'verbose_name': 'Page Legacy',
                'verbose_name_plural': 'Page Legacy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'PageType',
                'verbose_name_plural': 'PageTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrintingMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'PrintingMethod',
                'verbose_name_plural': 'PrintingMethods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publisher', models.TextField(default=b'', blank=True)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('publisherAbbrev', models.CharField(default=b'', max_length=45, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('cfeolabel', models.TextField(default=b'', blank=True)),
                ('ocve', models.BooleanField(default=False)),
                ('cfeo', models.BooleanField(default=False)),
                ('orderno', models.IntegerField(default=999)),
            ],
            options={
                'ordering': ['orderno'],
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orderno', models.IntegerField(null=True, blank=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('instrumentnumber', models.IntegerField(null=True, blank=True)),
                ('instrumentkey', models.CharField(default=b'', max_length=128, blank=True)),
                ('overridelabel', models.TextField(default=b'', blank=True)),
                ('sourcecomponenttitle', models.CharField(default=b'', help_text='e.g song titles like "Wojack"', max_length=255, blank=True)),
                ('source', models.ForeignKey(default=1, to='ocve.Source')),
            ],
            options={
                'ordering': ['orderno'],
                'verbose_name': 'SourceComponent',
                'verbose_name_plural': 'SourceComponents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceComponent_Instrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument', models.ForeignKey(to='ocve.Instrument')),
                ('sourcecomponent', models.ForeignKey(to='ocve.SourceComponent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceComponent_WorkComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sourcecomponent', models.ForeignKey(to='ocve.SourceComponent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceComponentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'SourceComponentType',
                'verbose_name_plural': 'SourceComponentTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platenumber', models.CharField(default=b'', max_length=255, blank=True)),
                ('locationsimilarcopies', models.TextField(default=b'', blank=True)),
                ('reprints', models.TextField(default=b'', blank=True)),
                ('seriestitle', models.CharField(default=b'', max_length=255, blank=True)),
                ('copyright', models.CharField(default=b'', max_length=255, blank=True)),
                ('contentssummary', models.CharField(default=b'', max_length=255, blank=True)),
                ('contents', models.TextField(default=b'', blank=True)),
                ('shelfmark', models.CharField(default=b'', max_length=255, blank=True)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('datepublication', models.CharField(default=b'', max_length=255, blank=True)),
                ('leaves', models.CharField(default=b'', max_length=255, blank=True)),
                ('sourcecode', models.CharField(default=b'', max_length=255, blank=True)),
                ('title', models.TextField(default=b'', blank=True)),
                ('publicationtitle', models.TextField(default=b'', blank=True)),
                ('imagesource', models.CharField(default=b'', max_length=255, blank=True)),
                ('additionalInformation', models.TextField(default=b'', blank=True)),
                ('keyFeatures', models.TextField(default=b'', blank=True)),
                ('volume', models.CharField(default=b'', max_length=255, blank=True)),
                ('displayedcopy', models.CharField(default=b'', max_length=255, blank=True)),
                ('accode', models.ForeignKey(default=1, to='ocve.AcCode')),
                ('archive', models.ForeignKey(default=1, to='ocve.Archive')),
                ('dedicatee', models.ForeignKey(default=1, to='ocve.Dedicatee')),
                ('placepublication', models.ForeignKey(blank=True, to='ocve.City', null=True)),
            ],
            options={
                'verbose_name': 'SourceInformation',
                'verbose_name_plural': 'SourceInformations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceInformation_PrintingMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('printingmethod', models.ForeignKey(to='ocve.PrintingMethod')),
                ('sourceinformation', models.ForeignKey(to='ocve.SourceInformation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceInformation_Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sourceinformation', models.ForeignKey(to='ocve.SourceInformation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceLegacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cfeoKey', models.IntegerField(default=0, null=True, blank=True)),
                ('witnessKey', models.IntegerField(default=0, null=True, blank=True)),
                ('sourceDesc', models.TextField(default=b'', blank=True)),
                ('mellon', models.BooleanField(default=False)),
                ('needsBarLines', models.BooleanField(default=False)),
                ('editstatus', models.ForeignKey(default=1, to='ocve.EditStatus')),
                ('source', models.ForeignKey(default=1, to='ocve.Source')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'SourceType',
                'verbose_name_plural': 'SourceTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'TreeType',
                'verbose_name_plural': 'TreeTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uncertain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pageimage', models.ForeignKey(to='ocve.PageImage')),
                ('source', models.ForeignKey(to='ocve.Source')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete', models.BooleanField(default=False)),
                ('label', models.TextField(default=b'', blank=True)),
                ('orderno', models.IntegerField(null=True, blank=True)),
                ('genre', models.ManyToManyField(default=1, to='ocve.Genre', through='ocve.Genre_Work')),
            ],
            options={
                'ordering': ['orderno'],
                'verbose_name': 'Work',
                'verbose_name_plural': 'Works',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('overridelabel', models.TextField(default=b'', blank=True)),
                ('collectiontype', models.ForeignKey(default=1, to='ocve.CollectionType')),
            ],
            options={
                'verbose_name': 'WorkCollection',
                'verbose_name_plural': 'WorkCollections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orderno', models.IntegerField(null=True, blank=True)),
                ('label', models.TextField(default=b'', blank=True)),
                ('music', models.IntegerField(null=True, blank=True)),
                ('keymode', models.ForeignKey(default=1, to='ocve.keyMode')),
                ('keypitch', models.ForeignKey(default=1, to='ocve.keyPitch')),
                ('opus', models.ForeignKey(default=1, to='ocve.Opus')),
                ('work', models.ForeignKey(default=1, to='ocve.Work')),
            ],
            options={
                'verbose_name': 'WorkComponent',
                'verbose_name_plural': 'WorkComponents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkComponentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'WorkComponentType',
                'verbose_name_plural': 'WorkComponentTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('generalinfo', models.TextField(default=b'', help_text='Publication History for this work', blank=True)),
                ('relevantmanuscripts', models.TextField(default=b'', blank=True)),
                ('analysis', models.TextField(default=b'', blank=True)),
                ('OCVE', models.TextField(default=b'', help_text='Only field displayed in OCVE work summary', blank=True)),
            ],
            options={
                'verbose_name': 'WorkInformation',
                'verbose_name_plural': 'WorkInformations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('sourceinformation', models.ManyToManyField(default=1, to='ocve.SourceInformation', through='ocve.SourceInformation_Year')),
            ],
            options={
                'ordering': ['year'],
                'verbose_name': 'Year',
                'verbose_name_plural': 'Years',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='work',
            name='workcollection',
            field=models.ForeignKey(default=2, to='ocve.WorkCollection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='workinformation',
            field=models.ForeignKey(default=1, to='ocve.WorkInformation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourceinformation_year',
            name='year',
            field=models.ForeignKey(to='ocve.Year'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourceinformation',
            name='printingmethod',
            field=models.ManyToManyField(default=1, to='ocve.PrintingMethod', through='ocve.SourceInformation_PrintingMethod'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourceinformation',
            name='publisher',
            field=models.ForeignKey(default=1, to='ocve.Publisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourceinformation',
            name='source',
            field=models.ForeignKey(default=1, to='ocve.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourcecomponent_workcomponent',
            name='workcomponent',
            field=models.ForeignKey(to='ocve.WorkComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourcecomponent',
            name='sourcecomponenttype',
            field=models.ForeignKey(default=1, to='ocve.SourceComponentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='sourcetype',
            field=models.ForeignKey(default=1, to='ocve.SourceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='pagetype',
            field=models.ForeignKey(default=1, to='ocve.PageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='sourcecomponent',
            field=models.ForeignKey(default=1, to='ocve.SourceComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsourceinformation',
            name='publisher',
            field=models.ForeignKey(default=1, to='ocve.Publisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsourceinformation',
            name='source',
            field=models.ForeignKey(default=1, to='ocve.NewSource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newpageimage',
            name='source',
            field=models.ForeignKey(default=1, to='ocve.NewSource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instrumentcomponent',
            name='sourcecomponent',
            field=models.ForeignKey(default=1, to='ocve.SourceComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instrument',
            name='sourcecomponent',
            field=models.ManyToManyField(to='ocve.SourceComponent', null=True, through='ocve.SourceComponent_Instrument', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genre_work',
            name='work',
            field=models.ForeignKey(to='ocve.Work'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(related_name='1', default=1, to='ocve.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barspine',
            name='source',
            field=models.ForeignKey(default=1, to='ocve.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barspine',
            name='sourcecomponent',
            field=models.ForeignKey(default=1, to='ocve.SourceComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barregion',
            name='page',
            field=models.ForeignKey(related_name='barRegions', default=1, to='ocve.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barregion',
            name='pageimage',
            field=models.ForeignKey(default=1, to='ocve.PageImage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='barcollection',
            name='regions',
            field=models.ManyToManyField(to='ocve.BarRegion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bar_barregion',
            name='barregion',
            field=models.ForeignKey(default=1, to='ocve.BarRegion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archive',
            name='city',
            field=models.ForeignKey(default=1, to='ocve.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='annotation_barregion',
            name='barregion',
            field=models.ForeignKey(to='ocve.BarRegion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='annotation',
            name='pageimage',
            field=models.ForeignKey(default=1, to='ocve.PageImage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='annotation',
            name='type',
            field=models.ForeignKey(default=1, to='ocve.AnnotationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='annotation',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
