# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import model_utils.fields
import wagtail.contrib.wagtailroutablepage.models
import django.utils.timezone
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0002_initial_data'),
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abbreviation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('abbreviation', models.CharField(unique=True, max_length=32)),
                ('description', wagtail.wagtailcore.fields.RichTextField()),
                ('slug', models.CharField(max_length=256, editable=False)),
            ],
            options={
                'ordering': ['abbreviation'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbbreviationIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('publisher_name', models.CharField(max_length=256)),
                ('publisher_name_slug', models.CharField(max_length=256, editable=False)),
                ('rubric', models.CharField(max_length=256)),
                ('rubric_slug', models.CharField(max_length=256, editable=False)),
                ('pdf', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'ordering': ['publisher_name', 'rubric'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdvertIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': "Publishers' Advertisements Index Page",
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Catalogue',
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Copies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlossaryIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='GlossaryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(unique=True, max_length=32)),
                ('description', wagtail.wagtailcore.fields.RichTextField()),
                ('slug', models.CharField(max_length=256, editable=False)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Impression',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('code_hash', models.CharField(max_length=32, editable=False)),
                ('impression_title', models.TextField()),
                ('comments', models.TextField()),
                ('content', models.TextField()),
                ('sort_order', models.PositiveIntegerField()),
                ('pdf', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'verbose_name': 'Impression',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ImpressionCopy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('copy', models.ForeignKey(to='catalogue.Copy')),
                ('impression', modelcluster.fields.ParentalKey(related_name='copies', to='catalogue.Impression')),
            ],
            options={
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=256)),
                ('library_url', models.URLField(null=True, blank=True)),
                ('city', models.ForeignKey(related_name='libraries', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='catalogue.City', null=True)),
                ('pdf', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'ordering': ['title', 'city', 'name'],
                'verbose_name_plural': 'Libraries',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LibraryIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Library Index Page',
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
                ('abbreviation', models.CharField(max_length=256, null=True, blank=True)),
                ('city', models.ForeignKey(related_name='publishers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='catalogue.City', null=True)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PublisherIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='RichTextPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='STP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('publisher_name', models.CharField(max_length=256)),
                ('publisher_name_slug', models.CharField(max_length=256, editable=False)),
                ('rubric', models.CharField(max_length=256)),
                ('rubric_slug', models.CharField(max_length=256, editable=False)),
                ('pdf', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
                ('publisher', models.ForeignKey(related_name='stps', blank=True, to='catalogue.Publisher', null=True)),
            ],
            options={
                'ordering': ['publisher_name', 'rubric'],
                'verbose_name': 'Series Title Page',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='STPIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Series Title Page Index Page',
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('code', models.CharField(max_length=32)),
                ('heading', models.TextField()),
                ('has_opus', models.BooleanField(default=False)),
                ('is_posthumous', models.BooleanField(default=False)),
                ('sort_order', models.PositiveIntegerField()),
                ('pdf', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Work',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterUniqueTogether(
            name='impressioncopy',
            unique_together=set([('impression', 'copy')]),
        ),
        migrations.AddField(
            model_name='impression',
            name='publisher',
            field=models.ForeignKey(related_name='impressions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='catalogue.Publisher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='copy',
            name='library',
            field=models.ForeignKey(to='catalogue.Library'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(related_name='cities', to='catalogue.Country'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('country', 'name')]),
        ),
        migrations.AddField(
            model_name='advert',
            name='publisher',
            field=models.ForeignKey(related_name='adverts', blank=True, to='catalogue.Publisher', null=True),
            preserve_default=True,
        ),
    ]
