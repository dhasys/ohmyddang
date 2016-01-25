# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'cms_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'cms', ['Category'])

        # Adding model 'Categories'
        db.create_table(u'cms_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Category'])),
        ))
        db.send_create_signal(u'cms', ['Categories'])

        # Adding M2M table for field sub_title on 'Categories'
        m2m_table_name = db.shorten_name(u'cms_categories_sub_title')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('categories', models.ForeignKey(orm[u'cms.categories'], null=False)),
            ('category', models.ForeignKey(orm[u'cms.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['categories_id', 'category_id'])

        # Adding model 'Option'
        db.create_table(u'cms_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option_name', self.gf('django.db.models.fields.TextField')()),
            ('option_count', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'cms', ['Option'])

        # Adding model 'Picture'
        db.create_table(u'cms_picture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('compress_image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Picture'])

        # Adding model 'Store'
        db.create_table(u'cms_store', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('manager_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('manager_phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('store_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('president_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('business_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('prime_image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prime_iamge', null=True, to=orm['cms.Picture'])),
            ('visible_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('activate_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('search', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('bank_code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('bank_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('store_pos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('store_layer', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('store_line', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('store_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('store_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'cms', ['Store'])

        # Adding M2M table for field pictures on 'Store'
        m2m_table_name = db.shorten_name(u'cms_store_pictures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('store', models.ForeignKey(orm[u'cms.store'], null=False)),
            ('picture', models.ForeignKey(orm[u'cms.picture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['store_id', 'picture_id'])

        # Adding model 'Member'
        db.create_table(u'cms_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('udid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('gender', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('push_acceptable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fake_download_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fake_coupon_used_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_fake_id', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('visible_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('push_id', self.gf('django.db.models.fields.CharField')(max_length=140, null=True)),
        ))
        db.send_create_signal(u'cms', ['Member'])

        # Adding model 'Coupon'
        db.create_table(u'cms_coupon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('original_price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('discount_price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='image2', null=True, to=orm['cms.Picture'])),
            ('visible_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('publish_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subscription_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('search', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('item_sub_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'cms', ['Coupon'])

        # Adding M2M table for field options on 'Coupon'
        m2m_table_name = db.shorten_name(u'cms_coupon_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'cms.coupon'], null=False)),
            ('option', models.ForeignKey(orm[u'cms.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'option_id'])

        # Adding M2M table for field pictures on 'Coupon'
        m2m_table_name = db.shorten_name(u'cms_coupon_pictures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'cms.coupon'], null=False)),
            ('picture', models.ForeignKey(orm[u'cms.picture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'picture_id'])

        # Adding model 'MyCoupon'
        db.create_table(u'cms_mycoupon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Coupon'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Member'])),
            ('useable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('usedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('subscription_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['MyCoupon'])

        # Adding model 'StoreReview'
        db.create_table(u'cms_storereview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Member'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['StoreReview'])

        # Adding model 'Like'
        db.create_table(u'cms_like', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Member'])),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Like'])

        # Adding model 'Visit'
        db.create_table(u'cms_visit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Member'])),
            ('visit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Visit'])

        # Adding model 'Board'
        db.create_table(u'cms_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('reply_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Board'])

        # Adding model 'BoardReply'
        db.create_table(u'cms_boardreply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Board'])),
            ('contents', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cms', ['BoardReply'])

        # Adding model 'Bill'
        db.create_table(u'cms_bill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill_type', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('point', self.gf('django.db.models.fields.IntegerField')()),
            ('visible_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'cms', ['Bill'])

        # Adding model 'MyBill'
        db.create_table(u'cms_mybill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Store'])),
            ('point', self.gf('django.db.models.fields.IntegerField')()),
            ('activated_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expired_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expense_type', self.gf('django.db.models.fields.IntegerField')()),
            ('expense_price', self.gf('django.db.models.fields.IntegerField')()),
            ('tid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('verify', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('useable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['MyBill'])

        # Adding model 'Notice'
        db.create_table(u'cms_notice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('display_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Notice'])

        # Adding model 'Push'
        db.create_table(u'cms_push', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('activated_date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('regdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Push'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'cms_category')

        # Deleting model 'Categories'
        db.delete_table(u'cms_categories')

        # Removing M2M table for field sub_title on 'Categories'
        db.delete_table(db.shorten_name(u'cms_categories_sub_title'))

        # Deleting model 'Option'
        db.delete_table(u'cms_option')

        # Deleting model 'Picture'
        db.delete_table(u'cms_picture')

        # Deleting model 'Store'
        db.delete_table(u'cms_store')

        # Removing M2M table for field pictures on 'Store'
        db.delete_table(db.shorten_name(u'cms_store_pictures'))

        # Deleting model 'Member'
        db.delete_table(u'cms_member')

        # Deleting model 'Coupon'
        db.delete_table(u'cms_coupon')

        # Removing M2M table for field options on 'Coupon'
        db.delete_table(db.shorten_name(u'cms_coupon_options'))

        # Removing M2M table for field pictures on 'Coupon'
        db.delete_table(db.shorten_name(u'cms_coupon_pictures'))

        # Deleting model 'MyCoupon'
        db.delete_table(u'cms_mycoupon')

        # Deleting model 'StoreReview'
        db.delete_table(u'cms_storereview')

        # Deleting model 'Like'
        db.delete_table(u'cms_like')

        # Deleting model 'Visit'
        db.delete_table(u'cms_visit')

        # Deleting model 'Board'
        db.delete_table(u'cms_board')

        # Deleting model 'BoardReply'
        db.delete_table(u'cms_boardreply')

        # Deleting model 'Bill'
        db.delete_table(u'cms_bill')

        # Deleting model 'MyBill'
        db.delete_table(u'cms_mybill')

        # Deleting model 'Notice'
        db.delete_table(u'cms_notice')

        # Deleting model 'Push'
        db.delete_table(u'cms_push')


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
            'item_sub_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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