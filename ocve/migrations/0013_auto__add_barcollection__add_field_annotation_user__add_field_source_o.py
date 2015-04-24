# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BarCollection'
        db.create_table('ocve_barcollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('xystring', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('ocve', ['BarCollection'])

        # Adding M2M table for field regions on 'BarCollection'
        m2m_table_name = db.shorten_name('ocve_barcollection_regions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('barcollection', models.ForeignKey(orm['ocve.barcollection'], null=False)),
            ('barregion', models.ForeignKey(orm['ocve.barregion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['barcollection_id', 'barregion_id'])

        # Adding field 'Annotation.user'
        db.add_column('ocve_annotation', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Source.orderno'
        db.add_column('ocve_source', 'orderno',
                      self.gf('django.db.models.fields.IntegerField')(default=999),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'BarCollection'
        db.delete_table('ocve_barcollection')

        # Removing M2M table for field regions on 'BarCollection'
        db.delete_table(db.shorten_name('ocve_barcollection_regions'))

        # Deleting field 'Annotation.user'
        db.delete_column('ocve_annotation', 'user_id')

        # Deleting field 'Source.orderno'
        db.delete_column('ocve_source', 'orderno')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ocve.accode': {
            'Meta': {'object_name': 'AcCode'},
            'accode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'accode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.AcCode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'noteregions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'notetext': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'pageimage': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.PageImage']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.AnnotationType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"})
        },
        'ocve.annotation_barregion': {
            'Meta': {'object_name': 'Annotation_BarRegion'},
            'annotation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Annotation']"}),
            'barregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.BarRegion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.annotationtype': {
            'Meta': {'object_name': 'AnnotationType'},
            'annotationType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.archive': {
            'Meta': {'ordering': "['name']", 'object_name': 'Archive'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'siglum': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.bar': {
            'Meta': {'ordering': "['barnumber', 'barlabel']", 'object_name': 'Bar'},
            'barlabel': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'barnumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.bar_barregion': {
            'Meta': {'object_name': 'Bar_BarRegion'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Bar']"}),
            'barregion': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.BarRegion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.barcollection': {
            'Meta': {'object_name': 'BarCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ocve.BarRegion']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"}),
            'xystring': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'ocve.barregion': {
            'Meta': {'object_name': 'BarRegion'},
            'annotation': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ocve.Annotation']", 'null': 'True', 'through': "orm['ocve.Annotation_BarRegion']", 'blank': 'True'}),
            'anomaly': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'bar': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ocve.Bar']", 'null': 'True', 'through': "orm['ocve.Bar_BarRegion']", 'blank': 'True'}),
            'barid_old': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'barRegions'", 'to': "orm['ocve.Page']"}),
            'pageimage': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.PageImage']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ocve.barsequence': {
            'Meta': {'object_name': 'BarSequence'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'endbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'startbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.barspine': {
            'Meta': {'object_name': 'BarSpine'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Bar']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'orderNo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Source']"}),
            'sourcecomponent': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.SourceComponent']"})
        },
        'ocve.city': {
            'Meta': {'object_name': 'City'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'1'", 'to': "orm['ocve.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.collectiontype': {
            'Meta': {'object_name': 'CollectionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.country': {
            'Meta': {'ordering': "['country']", 'object_name': 'Country'},
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'countryabbrev': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.dedicatee': {
            'Meta': {'ordering': "['dedicatee']", 'object_name': 'Dedicatee'},
            'alternateOf': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'alternate'", 'to': "orm['ocve.Dedicatee']"}),
            'dedicatee': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ocve.editstatus': {
            'Meta': {'ordering': "['id']", 'object_name': 'EditStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NONE'", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.genre': {
            'Meta': {'ordering': "['genre']", 'object_name': 'Genre'},
            'genre': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pluralname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.genre_work': {
            'Meta': {'object_name': 'Genre_Work'},
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Work']"})
        },
        'ocve.instrument': {
            'Meta': {'ordering': "['instrument']", 'object_name': 'Instrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'instrumentabbrev': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'sourcecomponent': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ocve.SourceComponent']", 'null': 'True', 'through': "orm['ocve.SourceComponent_Instrument']", 'blank': 'True'})
        },
        'ocve.instrumentcomponent': {
            'Meta': {'object_name': 'instrumentComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Instrument']"}),
            'sourcecomponent': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.SourceComponent']"})
        },
        'ocve.keymode': {
            'Meta': {'ordering': "['keymode']", 'object_name': 'keyMode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keymode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.keypitch': {
            'Meta': {'ordering': "['orderno']", 'object_name': 'keyPitch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keypitch': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'ocve.newpageimage': {
            'Meta': {'object_name': 'NewPageImage'},
            'corrected': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'endbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'permissionnote': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.NewSource']"}),
            'startbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'surrogate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'versionnumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ocve.newsource': {
            'Meta': {'object_name': 'NewSource'},
            'copyright': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'library': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sourcecode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sourcecreated': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'ocve.newsourceinformation': {
            'Meta': {'object_name': 'NewSourceInformation'},
            'accode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.AcCode']"}),
            'additionalInformation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Archive']"}),
            'contents': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contentssummary': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'datepublication': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'dedicatee': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Dedicatee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagesource': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'keyFeatures': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'leaves': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'locationsimilarcopies': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'platenumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'publicationtitle': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Publisher']"}),
            'reprints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'seriestitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'shelfmark': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.NewSource']"}),
            'sourcecode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.opus': {
            'Meta': {'ordering': "['opusno']", 'object_name': 'Opus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opusno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ocve.page': {
            'Meta': {'ordering': "['orderno']", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pagetype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.PageType']"}),
            'preferredversion': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'sourcecomponent': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.SourceComponent']"})
        },
        'ocve.pageimage': {
            'Meta': {'object_name': 'PageImage'},
            'corrected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'endbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Page']"}),
            'permission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'permissionnote': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'startbar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'surrogate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'versionnumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ocve.pagelegacy': {
            'Meta': {'object_name': 'PageLegacy'},
            'cfeoKey': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cropCorrected': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'editstatus': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.EditStatus']"}),
            'filename': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jp2': ('django.db.models.fields.CharField', [], {'default': "'UNVERIFIED'", 'max_length': '255', 'blank': 'True'}),
            'ocveKey': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pageimage': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.PageImage']"}),
            'storageStructure': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'ocve.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.printingmethod': {
            'Meta': {'object_name': 'PrintingMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.publisher': {
            'Meta': {'ordering': "['publisher']", 'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'publisher': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'publisherAbbrev': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45', 'blank': 'True'})
        },
        'ocve.source': {
            'Meta': {'ordering': "['label']", 'object_name': 'Source'},
            'cfeo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cfeolabel': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ocve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'default': '999'}),
            'sourcetype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.SourceType']"})
        },
        'ocve.sourcecomponent': {
            'Meta': {'ordering': "['orderno']", 'object_name': 'SourceComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrumentkey': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'instrumentnumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overridelabel': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Source']"}),
            'sourcecomponenttitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sourcecomponenttype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.SourceComponentType']"})
        },
        'ocve.sourcecomponent_instrument': {
            'Meta': {'object_name': 'SourceComponent_Instrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Instrument']"}),
            'sourcecomponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.SourceComponent']"})
        },
        'ocve.sourcecomponent_workcomponent': {
            'Meta': {'object_name': 'SourceComponent_WorkComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sourcecomponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.SourceComponent']"}),
            'workcomponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.WorkComponent']"})
        },
        'ocve.sourcecomponenttype': {
            'Meta': {'object_name': 'SourceComponentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.sourceinformation': {
            'Meta': {'object_name': 'SourceInformation'},
            'accode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.AcCode']"}),
            'additionalInformation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Archive']"}),
            'contents': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contentssummary': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'datepublication': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'dedicatee': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Dedicatee']"}),
            'displayedcopy': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagesource': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'keyFeatures': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'leaves': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'locationsimilarcopies': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'placepublication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.City']", 'null': 'True', 'blank': 'True'}),
            'platenumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'printingmethod': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['ocve.PrintingMethod']", 'through': "orm['ocve.SourceInformation_PrintingMethod']", 'symmetrical': 'False'}),
            'publicationtitle': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Publisher']"}),
            'reprints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'seriestitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'shelfmark': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Source']"}),
            'sourcecode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.sourceinformation_printingmethod': {
            'Meta': {'object_name': 'SourceInformation_PrintingMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printingmethod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.PrintingMethod']"}),
            'sourceinformation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.SourceInformation']"})
        },
        'ocve.sourceinformation_year': {
            'Meta': {'object_name': 'SourceInformation_Year'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sourceinformation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.SourceInformation']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Year']"})
        },
        'ocve.sourcelegacy': {
            'Meta': {'object_name': 'SourceLegacy'},
            'cfeoKey': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'editstatus': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.EditStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mellon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needsBarLines': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Source']"}),
            'sourceDesc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'witnessKey': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'ocve.sourcetype': {
            'Meta': {'object_name': 'SourceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.tree': {
            'Meta': {'object_name': 'Tree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orderNo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['ocve.Tree']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.TreeType']"})
        },
        'ocve.treetype': {
            'Meta': {'object_name': 'TreeType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        'ocve.uncertain': {
            'Meta': {'object_name': 'Uncertain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pageimage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.PageImage']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ocve.Source']"})
        },
        'ocve.work': {
            'Meta': {'ordering': "['orderno']", 'object_name': 'Work'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['ocve.Genre']", 'through': "orm['ocve.Genre_Work']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'workcollection': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': "orm['ocve.WorkCollection']"}),
            'workinformation': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.WorkInformation']"})
        },
        'ocve.workcollection': {
            'Meta': {'object_name': 'WorkCollection'},
            'collectiontype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.CollectionType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'overridelabel': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'ocve.workcomponent': {
            'Meta': {'ordering': "['orderno']", 'object_name': 'WorkComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keymode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.keyMode']"}),
            'keypitch': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.keyPitch']"}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'music': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'opus': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Opus']"}),
            'orderno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['ocve.Work']"})
        },
        'ocve.workcomponenttype': {
            'Meta': {'object_name': 'WorkComponentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'ocve.workinformation': {
            'Meta': {'object_name': 'WorkInformation'},
            'OCVE': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'analysis': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'generalinfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relevantmanuscripts': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'ocve.year': {
            'Meta': {'ordering': "['year']", 'object_name': 'Year'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sourceinformation': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['ocve.SourceInformation']", 'through': "orm['ocve.SourceInformation_Year']", 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ocve']