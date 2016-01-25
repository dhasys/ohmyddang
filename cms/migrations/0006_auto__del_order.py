# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'cms_order')

        # Removing M2M table for field options on 'Order'
        db.delete_table(db.shorten_name(u'cms_order_options'))


    def backwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'cms_order', (
            ('useable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subscription_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Coupon'])),
            ('usedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
        ))
        db.send_create_signal(u'cms', ['Order'])

        # Adding M2M table for field options on 'Order'
        m2m_table_name = db.shorten_name(u'cms_order_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm[u'cms.order'], null=False)),
            ('option', models.ForeignKey(orm[u'cms.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'option_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cms.bill': {
            'Meta': {'object_name': 'Bill'},
            'bill_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'visible_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'cms.board': {
            'Meta': {'object_name': 'Board'},
            'contents': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'reply_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'cms.boardreply': {
            'Meta': {'object_name': 'BoardReply'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Board']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cms.categories': {
            'Meta': {'object_name': 'Categories'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Category']"}),
            'sub_title': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sub_title'", 'symmetrical': 'False', 'to': u"orm['cms.Category']"})
        },
        u'cms.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cms.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'image2'", 'null': 'True', 'to': u"orm['cms.Picture']"}),
            'item_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_sub_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'item_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'options'", 'null': 'True', 'to': u"orm['cms.Option']"}),
            'original_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pictures2'", 'symmetrical': 'False', 'to': u"orm['cms.Picture']"}),
            'publish_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"}),
            'subscription_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'cms.like': {
            'Meta': {'object_name': 'Like'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Member']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"})
        },
        u'cms.member': {
            'Meta': {'object_name': 'Member'},
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fake_coupon_used_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fake_download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fake_id': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'push_acceptable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'udid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visible_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'cms.mybill': {
            'Meta': {'object_name': 'MyBill'},
            'activated_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expense_price': ('django.db.models.fields.IntegerField', [], {}),
            'expense_type': ('django.db.models.fields.IntegerField', [], {}),
            'expired_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"}),
            'tid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'useable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'verify': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'cms.mycoupon': {
            'Meta': {'object_name': 'MyCoupon'},
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Coupon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Member']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subscription_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'usedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cms.myorder': {
            'Meta': {'object_name': 'MyOrder'},
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Coupon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'myorder_options'", 'null': 'True', 'to': u"orm['cms.Option']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"}),
            'subscription_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'useable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'usedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cms.notice': {
            'Meta': {'object_name': 'Notice'},
            'contents': ('django.db.models.fields.TextField', [], {}),
            'display_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'cms.option': {
            'Meta': {'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'option_name': ('django.db.models.fields.TextField', [], {})
        },
        u'cms.picture': {
            'Meta': {'object_name': 'Picture'},
            'compress_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'cms.push': {
            'Meta': {'object_name': 'Push'},
            'activated_date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'cms.store': {
            'Meta': {'object_name': 'Store'},
            'activate_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bank_code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'bank_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'business_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'manager_phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pictures'", 'symmetrical': 'False', 'to': u"orm['cms.Picture']"}),
            'president_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'prime_image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prime_iamge'", 'null': 'True', 'to': u"orm['cms.Picture']"}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'store_layer': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'store_line': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'store_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'store_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'store_pos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'store_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'visible_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'cms.storereview': {
            'Meta': {'object_name': 'StoreReview'},
            'contents': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Member']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'regdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"})
        },
        u'cms.visit': {
            'Meta': {'object_name': 'Visit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Member']"}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Store']"}),
            'visit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cms']