from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.http import HttpResponse
import os


admin.autodiscover()

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

urlpatterns = patterns('',
  # Examples:
    # url(r'^$', 'funing_server.views.home', name='home'),
    # url(r'^funing_server/', include('funing_server.foo.urls')),

    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent:*\nDisallow:/", mimetype="text/plain")),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', u'cms.views.main'),
    url(r'^login/$', u'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', u'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^store/register/$', u'cms.views.store_register'),
    url(r'^store/register/save$', u'cms.views.store_register_save'),
    url(r'^store/register/activate/(\d+)/$', u'cms.views.store_register_activate'),
    url(r'^store/detail/(\d+)/$', u'cms.views.store_detail'),
    url(r'^store/modify/(\d+)/$', u'cms.views.store_register'),
    url(r'^store/list/$', u'cms.views.store_list'),
    url(r'^store/list/page/(\d+)/$', 'cms.views.store_list'),
    url(r'^store/login/(\d+)/$', 'cms.views.store_login'),
    url(r'^coupon/register/$', u'cms.views.coupon_register'),
    url(r'^coupon/register/save/$', u'cms.views.coupon_register_save'),
    url(r'^coupon/detail/(\d+)/$', u'cms.views.coupon_detail'),
    url(r'^coupon/modify/(\d+)/$', u'cms.views.coupon_register'),
    url(r'^coupon/list/(\w+)/$', u'cms.views.coupon_list'),
    url(r'^coupon/list/(\w+)/page/(\d+)/$', u'cms.views.coupon_list'),
    url(r'^coupon/toggle/(\d+)/$', u'cms.views.coupon_toggle'),


    url(r'^notice/register/$', u'cms.views.notice_register'),
    url(r'^notice/register/save/$', u'cms.views.notice_register_save'),
    url(r'^notice/detail/(\d+)/$', u'cms.views.notice_detail'),
    url(r'^notice/modify/(\d+)/$', u'cms.views.notice_register'),
    url(r'^notice/list/$', u'cms.views.notice_list'),
    url(r'^notice/list/page/(\d+)/$', u'cms.views.notice_list'),

    url(r'^board/register/$', u'cms.views.board_register'),
    url(r'^board/register/save/$', u'cms.views.board_register_save'),
    url(r'^board/detail/(\d+)/$', u'cms.views.board_detail'),
    url(r'^board/modify/(\d+)/$', u'cms.views.board_register'),
    url(r'^board/reply/modify/(\d+)/$', u'cms.views.board_reply'),
    url(r'^board/reply/(\d+)/$', u'cms.views.board_reply'),
    url(r'^board/reply/save/$', u'cms.views.board_reply_save'),
    url(r'^board/list/$', u'cms.views.board_list'),
    url(r'^board/list/page/(\d+)/$', u'cms.views.board_list'),

    url(r'^member/register/$', u'cms.views.member_register'),
    url(r'^member/register/save/$', u'cms.views.member_register_save'),
    url(r'^member/modify/(\d+)/$', u'cms.views.member_register'),
    url(r'^member/list/$', u'cms.views.member_list'),
    url(r'^member/list/page/(\d+)/$', u'cms.views.member_list'),
    url(r'^member/detail/(\d+)/$', u'cms.views.member_detail'),

    url(r'^push/register/$', u'cms.views.push_register'),
    url(r'^push/register/save/$', u'cms.views.push_register_save'),
    url(r'^push/modify/(\d+)/$', u'cms.views.push_register'),
    url(r'^push/list/$', u'cms.views.push_list'),
    url(r'^push/list/page/(\d+)/$', u'cms.views.push_list'),
    url(r'^push/detail/(\d+)/$', u'cms.views.push_detail'),
    url(r'^push/resent/(\d+)/$', u'cms.views.push_resent'),

    url(r'^point/register/$', u'cms.views.point_register'),
    url(r'^point/register/save/$', u'cms.views.point_register_save'),
    url(r'^point/list/$', u'cms.views.point_list'),
    url(r'^point/list/page/(\d+)/$', u'cms.views.point_list'),
    url(r'^point/payment/$', u'cms.views.point_payment'),
    url(r'^point/payment/page/(\d+)/$', u'cms.views.point_payment'),
    url(r'^point/payment/verify/$', u'cms.views.point_payment_verify'),
    url(r'^point/payment/result/$', u'cms.views.point_payment_success'),
    url(r'^point/payment/verify/success/$', u'cms.views.point_payment_verify_success'),
    url(r'^point/payment/failure/$', u'cms.views.point_payment_failure'),

    url(r'^review/register/$', u'cms.views.review_register'),
    url(r'^review/register/save/$', u'cms.views.review_register_save'),
    url(r'^review/detail/(\d+)/$', u'cms.views.review_detail'),
    url(r'^review/modify/(\d+)/$', u'cms.views.review_register'),
    url(r'^review/list/$', u'cms.views.review_list'),
    url(r'^review/list/page/(\d+)/$', u'cms.views.review_list'),

    url(r'^statistics/$', u'cms.views.statistics'),
    url(r'^statistics/(\w+)/$', u'cms.views.statistics'),
    url(r'^delete/(\w+)/(\d+)/$', u'cms.views.delete'),

    url(r'^popup/info$', u'cms.views.info_popup'),
    url(r'^popup/start$', u'cms.views.start_popup'),
    url(r'^popup/assent$', u'cms.views.assent_popup'),

    url(r'^api/s/geo$', u'api.views.get_address_geo'),
    url(r'^api/s/geo/location$', u'api.views.get_geo_location'),
    url(r'^api/s/geo/address$', u'api.views.get_geo_address'),
    url(r'^api/s/idcheck$', u'api.views.store_validate'),
    url(r'^api/s/coupon/point$', u'api.views.coupon_point_check'),
    url(r'^api/s/payment/verify$', u'api.views.set_mybill_verify'),

    url(r'^api/c/member/register$', u'api.views.member_register'),
    url(r'^api/c/member/login$', u'api.views.member_login'),
    url(r'^api/c/member/push$', u'api.views.member_push'),
   
    url(r'^api/c/store/register$', u'api.views.store_register'),
    url(r'^api/c/store/list$', u'api.views.store_list'),
    url(r'^api/c/store/set/(\w+)/$', u'api.views.set_store_from_jsonfile'),
    url(r'^api/c/store/detail$', u'api.views.store_detail'),
    url(r'^api/c/store/like$', u'api.views.store_like'),
    url(r'^api/c/store/login$', u'api.views.store_login'),
    url(r'^api/c/store/statistics$', u'api.views.store_statistics'),
    url(r'^api/c/store/point$', u'api.views.store_point'),
    
    url(r'^api/c/coupon/list$', u'api.views.coupon_list'),
    url(r'^api/c/coupon/use$', u'api.views.coupon_use'),
    url(r'^api/c/coupon/add$', u'api.views.coupon_add'),
    url(r'^api/c/coupon/detail$', u'api.views.coupon_detail'),
    url(r'^api/c/coupon/register$', u'api.views.coupon_register'),
    url(r'^api/c/coupon/toggle$', u'api.views.coupon_toggle'),
    
    url(r'^api/c/order/list$', u'api.views.order_list'),
    
    
    url(r'^api/c/review/list$', u'api.views.review_list'),
    url(r'^api/c/review/add$', u'api.views.review_add'),
    url(r'^api/c/review/delete$', u'api.views.review_delete'),
    url(r'^api/c/notice/list$', u'api.views.notice_list'),
    url(r'^api/c/push/send$', u'api.views.push_message_send'),
    url(r'^api/c/mail/send$', u'api.views.mail_send'),
     
    url(r'^api/c/category/list$', u'api.views.categories_list'), 
    
)
