# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from cms.models import *
from cms.views import *
from common import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
from datetime import timedelta
from django.db.models import Sum
from operator import attrgetter
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext
import httplib2
import urllib
import simplejson as json
import logging
import hashlib
import time
from django.contrib.admin.templatetags.admin_list import results
from _ast import Subscript
from __builtin__ import True

logger = logging.getLogger(__name__)

_COUPON_POINT = 50

# _DAUM_LOCAL_API_KEY = 'a6a2abd567e7fada37f13bbd1d19c06313592a8e'  # release
#_DAUM_LOCAL_API_KEY = 'f22ef881b6ebcf011b3e954ab5745662c4d4a0f8'  # develop
_DAUM_LOCAL_API_KEY = 'b31471992fe548fac1128c60f1af102c8f616ab1'



def get_address_geo(request):
    req = request.GET
    address = req['address']
    address = urllib.quote(address.encode('utf-8'))
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&sensor=true"
    response, content = httplib2.Http().request(url, "GET")

    return HttpResponse(content)


def get_geo_location(request):
    req = request.GET
    lat = req['lat']
    lng = req['lng']
    url = "http://apis.daum.net/local/geo/coord2addr?apikey=" + _DAUM_LOCAL_API_KEY + "&longitude=" + lng + "&latitude=" + lat + "&output=json"
    response, content = httplib2.Http().request(url, "GET")
    data = json.loads(content)

    return HttpResponse(data['fullName'])


def get_geo_address(request):
    print "1"
    req = request.GET
    address = req['address'].strip().replace(" ", "")
    url = "http://apis.daum.net/local/geo/addr2coord?apikey=" + _DAUM_LOCAL_API_KEY + "&q=" + address + "&output=json"
    response, content = httplib2.Http().request(url, "GET")
   
    data = json.loads(content)
    print data
 
    channel = data['channel']
    #print "2"

    #print channel

    totalCount = channel['totalCount']
    print totalCount

    result = {}
    if totalCount > 0:
        item = channel['item']
        item = item[0]
        result['lng'] = item['lng']
        result['lat'] = item['lat']
        print result

    return HttpResponse(json.dumps(result).encode('utf-8'))


def set_mybill_verify(request):
    result = 'fail'
    req = request.GET
    tid = req['tid']
    mybill = MyBill.objects.filter(tid=tid)
    if len(mybill) > 0:
        mybill = mybill[0]
        mybill.verify = True
        mybill.save()
        result = 'success'

    return HttpResponse(result)


def store_validate(request):
    if request.method == "GET":
        result = '성공'
        req = request.GET
        store_id = req['id']
        check_id = User.objects.filter(username=store_id).count()
        if check_id > 0:
            result = 'id 가 중복되었습니다.'
        else:
            store_email = req['email']
            check_email = User.objects.filter(email=store_email).count()
            if check_email > 0:
                result = 'email이 중복되었습니다.'

    return HttpResponse(result)


def coupon_point_check(request):
    result = 0
    original_count = 0
    return_data = ''
    store_id = ''
    coupon_count = 0
    if request.method == 'GET':
        req = request.GET
        coupon_count = int(req['count'])
    elif request.method == 'POST':
        req = request.POST
        coupon_count = int(req['coupon_count'])

    store_id = req['s_id']
    coupon_id = int(req['c_id'])

    if int(coupon_id) > 0:
        coupon = Coupon.objects.get(id=coupon_id)
        status = get_coupon_status(coupon)
        if status == u'발행대기':
            original_count = coupon.count
        else:
            coupon_id = 0

    results = get_coupon_extra_point(store_id)

    if results['result']:
        if results['subscription']:
            return_data = '정액제'
        else:
            extra_point = results['extrapoint']
            if extra_point < 0:
                return_data = result
            else:
                available_cnt = int(results['available_cnt'])
                if coupon_id > 0:
                    # 쿠폰수정할때.
                    if coupon.subscription_flag == False:
                        # 정액제가 아닌쿠폰이 수정될때.
                        available_cnt += original_count
                if available_cnt < coupon_count:
                    # 등록가능한 쿠폰수
                    return_data = result
                else:
                    result = '성공'
                    return_data = result

    if request.method == 'GET':
        return HttpResponse(return_data)
    elif request.method == 'POST':
        return return_data



@csrf_exempt
def member_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
    if request.method == "GET":
        #data = request.GET
        data = {'member_id': "359670030454514", 'member_nickname': 'sky vega1'}
        
    print  request.method , data
    
    if 'isResponse' in data:
        if data['isResponse'] == 'true':
            return member_login_duplicate_check(data)
    else:

        #return HttpResponse(json.dumps(member_register_save(request, data)).encode('utf-8'))

        return HttpResponse(json.dumps(member_register_save(request, data['data'])).encode('utf-8'))


@csrf_exempt
# @gzip_page
def member_login(request):
    #print request.get_request()
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
         json_data = {'udid': "352316052182585"}

    result = member_login_check(json_data['udid'])

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def store_register(request):
    if request.method == "POST":
        #data = {'store_id': "test1699", "password" : "11", "email" : "test@naver.com" , "store_name" : "test11", "president_name" : "1", "business_number" : "01020055915", "manager_phone" : "01020055915", "manager_name" : "1"} 

        data = json.loads(request.body)
        return HttpResponse(json.dumps(store_register_save_1(request, data['data'])).encode('utf-8'))

    else:
        data = {'store_id': "test11", "password" : "11", "email" : "test@naver.com" , "store_name" : "test11", "president_name" : "1", "business_number" : "01020055915", "manager_phone" : "01020055915", "manager_name" : "1"} 
        return HttpResponse(json.dumps(store_register_save_1(request, data)).encode('utf-8'))




@csrf_exempt
@gzip_page
def store_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'lng': 37.498741, 'lat': 127.043144}

    store_list = get_store_list(json_data)
    result = json.dumps(list(store_list))

    return HttpResponse(result)


@csrf_exempt
def set_store_from_jsonfile(request, json_file='store'):
    # json_data = open(settings.JSON_ROOT + '/store.json')
    json_data = open(settings.JSON_ROOT + '/' + json_file + '.json')
    store = json.load(json_data)

    json_data.close()
    result = ''
    for s in store:
        result += '<p>' + set_store(s) + '</p>'

    return HttpResponse(result)


@csrf_exempt
@gzip_page
def store_detail(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        # type : 'merchant', 'store'
        # json_data = {'member_id': '1', 'store_id': '1', 'type': 'store'}
        json_data = {'member_id': '1', 'store_id': '1', 'type': 'store'}

    result = get_store_detail_info(json_data)

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def store_like(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': '352316052182585', 'sid': 'nrise'}

    result = set_store_like(json_data)

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def store_login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'username': 'nrise', 'password': '1234'}

    result = check_store_login(json_data)

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
@gzip_page
def coupon_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'type': 'my', 'id': '1'}

    today = datetime.datetime.today()
    if 'type' in json_data:
        if json_data['type'] == 'my':
            # 내 쿠폰 리스트
            store = Store.objects.get(id=int(json_data['id']))
            arr = MyOrder.objects.filter(store=store, useable=True).order_by('-regdate')
            coupon = []
            for item in arr:
                coupon.append(item.coupon)
        elif json_data['type'] == 'store':
            # 해당 상점이 발행중인 쿠폰 리스트
            store = Store.objects.get(id=int(json_data['id']))
            if len(store_check(store)) > 0:
                coupon = []
                coupons = Coupon.objects.filter(visible_flag=True, publish_flag=True, store=store).order_by('-regdate')
                for cp in coupons:
                    coupon.append(cp)
            else:
                coupon = []
        elif json_data['type'] == 'merchant':
            # 해당 상점의 모든 쿠폰 리스트
            store = Store.objects.get(id=int(json_data['id']))
            coupon = Coupon.objects.filter(visible_flag=True, store=store).order_by('-regdate')
        elif json_data['type'] == 'search':
            # 사용자가 검색한 쿠폰 리스트
            store_list = store_check()
            coupon = []
            for store in store_list:
                coupons = Coupon.objects.filter(store=store, name__contains=json_data['query'], visible_flag=True, publish_flag=True).order_by('-regdate')
                for cp in coupons:
                    mycoupon_cnt = MyOrder.objects.filter(coupon=cp).count()
                    if cp.count > mycoupon_cnt and check_coupon_time(cp):
                        coupon.append(cp)

            coupon.sort(key=attrgetter('regdate'), reverse=True)
        elif json_data['type'] == 'merchant_search':
            # 상점주가 검색한 쿠폰 리스트
            store = Store.objects.get(id=int(json_data['id']))
            coupon = Coupon.objects.filter(visible_flag=True, name__contains=json_data['query'], store=store).order_by('-regdate')
        elif json_data['type'] == 'favorite':
            store_list = store_check()
        
            for store in store_list:
                coupons = Coupon.objects.filter(store=store, visible_flag=True, publish_flag=True).order_by('-regdate')
                for cp in coupons:
                    coupon.append(cp)

            coupon.sort(key=attrgetter('regdate'), reverse=True)
            
        else:
            # 발행중인 모든 쿠폰 리스트
            store_list = store_check()
            coupon = []
            for store in store_list:
                coupons = Coupon.objects.filter(store=store, visible_flag=True, publish_flag=True).order_by('-regdate')
                for cp in coupons:
                    #mycoupon_cnt = MyCoupon.objects.filter(coupon=cp).count()
                    #if cp.count > mycoupon_cnt: #and check_coupon_time(cp):
                        # 쿠폰등록시 입력한 개수보다 다운수가 많을경우는 목록에서 안보여줌.
                    coupon.append(cp)

            coupon.sort(key=attrgetter('regdate'), reverse=True)
            # if json_data['type'] == 'widget':
            #     if len(coupon) > 10:
            #         coupon = coupon[:10]

    data = []
    for item in coupon:
        dic = {}
        dic['id'] = item.id
        dic['name'] = item.name
        dic['sId'] = item.store.id
        dic['sName'] = item.store.store_name
        dic['org'] = item.original_price
        dic['dis'] = item.discount_price
        
        dic['count'] = item.count
        
        #category = Categories.objects.get(id=item.)
        dic['main_category'] = item.item_type
        #dic['main_category_title'] = category.main_title.name
      
        #sub = category.sub_title.all()[0]
        dic['sub_category'] = item.item_sub_type
        #dic['sub_category_id'] = category.main_title.name
        
    
        if item.image is not None:
            dic['img'] = item.image.compress_image.url

        if json_data['type'] == 'merchant' or json_data['type'] == 'merchant_search':
            # 발행중 1 , 발행대기 2 , 발행중지 3, 기존상품 4
            status = get_coupon_status(item)
            dic['comment'] = status
            if status == u'발행중':
                dic['status'] = 1
            elif status == u'발행중지':
                dic['status'] = 3

            dic['use'] = MyCoupon.objects.filter(coupon=item).count()

        
        temps = []
        
        if json_data['type'] == 'my':
            order = MyOrder.objects.filter(store=store, useable=True).order_by('-regdate')
        else:                  
            options = item.options.all()
            for opt in options:    
                temp = {}
                temp['id'] = opt.id
                temp['name'] = opt.option_name
                temp['count'] = opt.option_count
                temps.append(temp)
        
        if (len(temps) > 0) :    
           dic['option'] = temps
           

            
            
        data.append(dic)
    return HttpResponse(json.dumps(data))


@csrf_exempt
def coupon_detail(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'coupon_id': 1, 'member_id': 1, 'type': 'merchant'}

    coupon = Coupon.objects.filter(id=json_data['coupon_id'])[0]

    result = {}
    if json_data['type'] == 'merchant':
        result['count'] = coupon.count
            
    else:
        result['sId'] = coupon.store.id
        #result['sAdr1'] = coupon.store.address
        #result['work'] = u'%s:%s-%s:%s' % (coupon.store.open_time[0:2], coupon.store.open_time[2:], coupon.store.close_time[0:2], coupon.store.close_time[2:])

        member = Member.objects.filter(id=json_data['member_id'])[0]
        today = datetime.datetime.today()
        mycoupon = MyCoupon.objects.filter(member=member, coupon=coupon, useable=True, regdate__year=today.year, regdate__month=today.month, regdate__day=today.day)
        if mycoupon.count() > 0:
            result['downFlag'] = 'YES'
            myCoupon = mycoupon[0]
            result['useable'] = myCoupon.useable
        else:
            result['downFlag'] = 'NO'
            result['useable'] = False

    result['description'] = coupon.description
    if coupon.image is not None:
            result['image'] = coupon.image.original_image.url

    temps = []
    options = coupon.options.all()
    for opt in options:    
        temp = {}
        temp['name'] = opt.option_name
        temp['count'] = opt.option_count
        temps.append(temp)
    
    if (len(temps) > 0) :    
       result['option'] = temps
       
    result['name'] = coupon.name
    result['org'] = coupon.original_price
    result['dis'] = coupon.discount_price
    #if coupon.discount_percentage is not None:
    #    result['rate'] = coupon.discount_percentage
    

    return HttpResponse(json.dumps(result).encode('utf-8'))


def store_check(__store=None):
    today = datetime.datetime.today()
    store = []
    if __store is None:
        store = Store.objects.all()
    else:
        store.append(__store)

    store_list = []
    # 쿠폰 포인트의 디폴트값이 정해져 있어야함.
    # get_store_detail_info 에서도 사용중.
    for s in store:
        mybill = MyBill.objects.filter(store=s, useable=True)
        if len(mybill.filter(activated_date__lte=today, expired_date__gte=today)) > 0:
            # 정액제 사용중.
            store_list.append(s)
        else:
            if len(mybill.filter(expired_date=None)) > 0:
                sum_point = mybill.filter(expired_date=None).aggregate(Sum('point'))['point__sum']
                use_point = MyCoupon.objects.filter(coupon__store=s, subscription_flag=False).count() * _COUPON_POINT
                if sum_point > use_point:
                    store_list.append(s)

    return store_list


@csrf_exempt
def coupon_add(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'store_id': 1, 'coupon_id': 6}
        datas = []
        data1 = {}
        data1['name'] = 'color_yellow' 
        data1['count'] = '10'
        #print data1  
        datas.append(data1)
        
        #print datas
                 
        json_data['option_type'] = datas
        

    print json_data

    result = {}
    result['result'] =  True
    result['msg'] = u'쿠폰 등록 성공.'
    today = datetime.datetime.today()
    coupon = Coupon.objects.filter(visible_flag=True, publish_flag=True, id=int(json_data['coupon_id']))
    #coupon = Coupon.objects.filter(visible_flag=True, publish_flag=True, id=int(json_data['coupon_id']))

    if len(coupon) != 1:
        result['result'] = False
        result['msg'] = u'유효하지 않은 아이 번호 입니다.'
        print result
        return HttpResponse(json.dumps(result).encode('utf-8'))
    else:
        coupon = coupon[0]
        if coupon.count == MyCoupon.objects.filter(coupon=coupon).count():
            result['result'] =False
            result['msg'] = u'남은 수량이 없습니다.'
            return HttpResponse(json.dumps(result).encode('utf-8'))

        store = Store.objects.filter(id=coupon.store.id)
        if len(store) == 1:
            point_result = get_coupon_extra_point(store[0].id)
            if point_result['subscription'] == False and point_result['extrapoint'] == 0:
                result['result'] = False
                result['msg'] = u'남은 금액이 없습니다.'
                return HttpResponse(json.dumps(result).encode('utf-8'))
        else:
            result['result'] = False
            result['msg'] = u'유효하지 않은 아이템 정보입니다.'
            return HttpResponse(json.dumps(result).encode('utf-8'))

    subscription_flag = False
    mybill = MyBill.objects.filter(store=coupon.store, useable=True, activated_date__lte=today, expired_date__gte=today)
    if len(mybill) == 1:
        subscription_flag = True

    store = Store.objects.filter(id=json_data['store_id'])
    if len(store) == 0:
        result['result'] = False
        result['msg'] = u'유효하지 않은 사용자입니다.'
        
    store = store[0]

    order = MyOrder.objects.filter(coupon=coupon, store=store)
    #order = MyOrder.filter(regdate__year=int(today.year), regdate__month=int(today.month), regdate__day=int(today.day), useable=True)
    if len(order) > 0:
        result['result'] = False
        result['msg'] = u'해당 사용자는 해당 아이템을 이미 등록하였습니다.'
        return HttpResponse(json.dumps(result).encode('utf-8'))

    order = MyOrder()
    order.coupon = coupon
    order.store = store
    order.subscription_flag = subscription_flag
    order.save()
    
    if 'option_type' in json_data:
        datas = []
        datas = json_data['option_type']
    
        for data in datas:
            
            option = Option()
            option.option_name = data['name']
            option.option_count = data['count']
            option.save()
            order.options.add(option)
            
        coupon.save()
                

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def coupon_use(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'member_id': 1, 'coupon_id': 106, 'num': 83676}

    today = datetime.datetime.today()
    result = {}
    result['result'] = 'ok'
    result['msg'] = u'쿠폰 인증 성공.'

    coupon = Coupon.objects.filter(id=json_data['coupon_id'])
    if len(coupon) == 1:
        store = Store.objects.get(id=coupon[0].store.id)
        if str(store.business_number)[5:] != str(json_data['num']):
            result['result'] = 'fail'
            result['msg'] = u'쿠폰 인증번호가 일치하지않습니다.'
        else:
            coupon = coupon[0]
            member = Member.objects.filter(id=json_data['member_id'])
            if len(member) == 0:
                result['result'] = 'fail'
                result['msg'] = u'유효하지 않은 사용자입니다.'
            member = member[0]

            mycoupon = MyCoupon.objects.filter(coupon=coupon, member=member, useable=True)
            if len(mycoupon) != 1:
                result['result'] = 'fail'
                result['msg'] = u'사용할 수 있는 쿠폰이 존재하지 않습니다.'
            else:
                if coupon.expired_date_time < today:
                    result['result'] = 'fail'
                    result['msg'] = u'사용기간이 만료된 쿠폰입니다.'
                else:
                    # 쿠폰의 사용
                    mycoupon = mycoupon[0]
                    mycoupon.useable = False
                    mycoupon.save()
    else:
        result['result'] = 'fail'
        result['msg'] = u'유효하지 않은 쿠폰 번호 입니다.'

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def coupon_register(request):
    # 쿠폰 저장시 상점의 포인트를 비교하여서 저장 가능한지 체크.
    #result = coupon_point_check(request)

    #if result == '정액제' or result == '성공':
    
    if request.method == "POST":
        result = coupon_register_save(request)
    else:
        #print '1'
        data = {}
        data['c_id'] = '0'
        data['s_id'] = '1'
        data['coupon_name'] = 'test'
        data['description'] = '11'
        data['coupon_count'] = '11'
        data['discount_type'] = '0'
        data['original_price'] = '100'
        data['discount_price'] = '90'
        data['type'] = ''
        
        #print data
        
        datas = []
        data1 = {}
        data1['name'] = 'color_yellow' 
        data1['count'] = '10'
        #print data1
        
        
        data2 = {}
        data2['name'] = 'color_red' 
        data2['count'] = '5'
        #print data2
        
        datas.append(data1)
        datas.append(data2)
        
        #print datas
                 
        data['option_type'] = datas
        
        #print data
         
        result = coupon_register_save(request, data)
    #elif result is 0:
    #    result = {'result': False, 'msg': '쿠폰 포인트가 부족합니다.'}

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def review_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': 2}

    store = Store.objects.get(id=json_data['id'])
    review = StoreReview.objects.filter(store=store).order_by('-regdate')

    results = []
    for item in review:
        result = {}
        result['review_id'] = item.id
        if item.member == None:
            result['name'] = item.name
        else:
            result['name'] = item.member.nickname
            result['member_id'] = item.member.id

        result['review'] = item.contents
        result['date'] = str(item.regdate)[0:19]
        results.append(result)

    return HttpResponse(json.dumps(results).encode('utf-8'))


@csrf_exempt
def category_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': 2}

    categories = Categories.objects.all
   
    results = []
    return HttpResponse(json.dumps(results).encode('utf-8'))




@csrf_exempt
def review_add(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'store_id': 1, 'member_id': 1, 'content': u'티모는 충이다'}

    member = Member.objects.get(id=json_data['member_id'])
    store = Store.objects.get(id=json_data['store_id'])
    review = StoreReview()
    review.member = member
    review.name = member.nickname
    review.store = store
    review.contents = json_data['content']
    review.save()

    return HttpResponse(json.dumps({'result': 'ok', 'review_id': review.id}).encode('utf-8'))


@csrf_exempt
def review_delete(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'member_id': 2, 'review_id': 2}

    member = Member.objects.get(id=json_data['member_id'])
    review = StoreReview.objects.filter(member=member, id=json_data['review_id'])
    if len(review) != 1:
        return HttpResponse(json.dumps({'result':'fail', 'code':1, 'msg':u'삭제 대상 리뷰가 존재하지 않거나 1개 이상입니다.'}).encode('utf-8'))
    review[0].delete()

    return HttpResponse(json.dumps({'result':'ok'}).encode('utf-8'))


@csrf_exempt
def notice_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        #json_data = {'display':'main'}
        json_data = {}

    display_flag = False
    notice = Notice.objects.filter().order_by('-regdate')
    if 'display' in json_data and json_data['display'] == 'main':
        display_flag = True
        notice = Notice.objects.filter(display_flag=display_flag).order_by('-regdate')

    results = []
    for item in notice:
        result = {}
        result['id'] = item.id
        result['title'] = item.title
        result['content'] = item.contents
        result['date'] = str(item.regdate)[0:19]
        results.append(result)

    return HttpResponse(json.dumps(results).encode('utf-8'))


@csrf_exempt
def coupon_toggle(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': '41'}

    cp = Coupon.objects.filter(id=json_data['id'])
    results = {}
    if len(cp) != 0:
        cp = Coupon.objects.get(id=json_data['id'])
        cp.publish_flag = not cp.publish_flag
        cp.save()
        results = {'result': True}
    else:
        results = {'result': False}

    return HttpResponse(json.dumps(results).encode('utf-8'))


@csrf_exempt
def store_statistics(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': '1'}

    store_id = json_data['id']

    results = {}
    today = datetime.datetime.today()

    delta = timedelta(days=7)
    delta_month = timedelta(days=31)
    week_start = today - delta
    month_start = today - delta_month
    visit = Visit.objects.filter(store=store_id)
    my_coupon = MyCoupon.objects.filter(coupon__store=store_id)

    today_visit = visit.filter(visit_date__year=today.year, visit_date__month=today.month, visit_date__day=today.day).count()
    today_down = my_coupon.filter(regdate__year=today.year, regdate__month=today.month, regdate__day=today.day).count()
    today_use = my_coupon.filter(useable=False, usedate__year=today.year, usedate__month=today.month, usedate__day=today.day).count()

    week_visit = visit.filter(visit_date__gt=week_start, visit_date__lte=today).count()
    week_down = my_coupon.filter(regdate__gt=week_start, regdate__lte=today).count()
    week_use = my_coupon.filter(usedate__gte=week_start, usedate__lte=today, useable=False).count()

    month_visit = visit.filter(visit_date__gt=month_start, visit_date__lte=today).count()
    month_down = my_coupon.filter(regdate__gt=month_start, regdate__lte=today).count()
    month_use = my_coupon.filter(useable=False, usedate__gte=month_start, usedate__lte=today).count()

    total_visit = visit.count()
    total_down = my_coupon.count()
    total_use = my_coupon.filter(useable=False).count()

    results['today_visit'] = today_visit
    results['today_down'] = today_down
    results['today_use'] = today_use

    results['week_visit'] = week_visit
    results['week_down'] = week_down
    results['week_use'] = week_use

    results['month_visit'] = month_visit
    results['month_down'] = month_down
    results['month_use'] = month_use

    results['total_visit'] = total_visit
    results['total_down'] = total_down
    results['total_use'] = total_use

    return HttpResponse(json.dumps(results).encode('utf-8'))


@csrf_exempt
def member_push(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': '352316052182585', 'push_id': 'APA91bHDDzzcfmSrHGhsj7JemwalHWminvtNe75Xwny0vcUHXvW-gWRoPeOwlwTn2_oGJaSX3HlePHgDn_JdTZmHCGyofroZk0NvqIIlAZTvpZq68ccRWDN7VAFplBut-8x2tAXy3thy', 'enable': True}
        # json_data = {'id': '1', 'reg_id': '123123123', 'enable': False}

    results = results = {'result': False}
    members = Member.objects.filter(id=json_data['id'])
    if len(members) > 0:
        member = Member.objects.get(id=json_data['id'])
        if json_data['enable'] is True:
            # 등록
            member.push_acceptable = True
            if len(json_data['push_id']) > 0:
                member.push_id = json_data['push_id']
            results = {'result': True}
        else:
            # 비활성화
            member.push_acceptable = False
        member.save()

    return HttpResponse(json.dumps(results).encode('utf-8'))


@csrf_exempt
def push_message_send(request):
    return HttpResponse()


@csrf_exempt
def store_point(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'id': '2'}

    result = {}
    results = get_coupon_extra_point(json_data['id'])
    if results['result'] is True:
        if results['subscription'] is True:
            result['point'] = -1
        else:
            result['point'] = int(results['available_cnt'])

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def mail_send(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'mail': 'sunken37@gmail.com'}

    # 메일을 비교하여서 그러한 이메일이 있는 지 체크.
    users = User.objects.filter(email=json_data['mail'])
    result = {'result': True}
    if len(users) > 0:
        user = users[0]
        # 해당 메일주소의 User 비밀번호를 수정하고 해당 비밀번호를 저장.
        password = hashlib.sha256(str(time.time())).hexdigest()
        user.set_password(password[:5])
        user.save()
        # 변경된 비밀번호를 입력받은 메일주소로 유저에게 메일 전송.
        send_mail('Funing 가맹점 비밀번호 전송', '임시 비밀번호를 알려드립니다 : ' + password[:5], 'no-reply@funing.co.kr', [json_data['mail']], fail_silently=False)
    else:
        result = {'result': False}

    return HttpResponse(json.dumps(result).encode('utf-8'))


@csrf_exempt
def hello(request):
    logger.error('Something went wrong!')
    variables = RequestContext(request)
    dictionary = {}
    return render_to_response('hello.html', dictionary, variables)



@csrf_exempt
def categories_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'type': '', 'id': '13'}

    categories = Categories.objects.all()
   
    result = {'result': True}
    if len(categories) > 0:
            
        datas = []
       
        for data in categories:
            main = {}
            main['main_category'] = data.main_title.name
            subs = []
            for subdata in data.sub_title.all():
                subs.append(subdata.name)
               
            main['sub_category'] = subs
            datas.append(main)
    
        result['data'] = datas
    
    else:
        result = {'result': False}
    
    return HttpResponse(json.dumps(result).encode('utf-8'))

@csrf_exempt
@gzip_page
def order_list(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
    else:
        json_data = {'type': 'my', 'id': '3'}

    today = datetime.datetime.today()
    if 'type' in json_data:
        if json_data['type'] == 'my':
            # 내 쿠폰 리스트
            store = Store.objects.get(id=int(json_data['id']))
            order = MyOrder.objects.filter(store=store).order_by('-regdate')
            if len(order) < 1 :
                data = {}
                data['result'] = False
                data['msg'] = "주문 내역이 없습니다."
                return HttpResponse(json.dumps(data))
            
          
         
    data = {} 
    datas = []
    for item in order:
        coupon = item.coupon
        dic = {}
        dic['id'] = item.id
        dic['name'] = coupon.name
        dic['cid'] = '1{:02d}{:d}{:d}{:04d}'.format(item.store.id, coupon.item_type, coupon.item_sub_type, coupon.id)
        dic['regdate'] = str(item.regdate)[0:19]
        
          
        dic['main_category'] = coupon.item_type
        dic['sub_category'] =coupon.item_sub_type
        
        if coupon.image is not None:
            dic['img'] = coupon.image.compress_image.url

        total_cnt = item.options.all().aggregate(Sum('option_count'))['option_count__sum']
        price_sum = total_cnt * coupon.discount_price
        dic['price'] = price_sum
        dic['count'] = total_cnt
        
        
        status = get_order_status(item)     
        dic['status_txt'] = status
        dic['status'] = item.status
        
            
        datas.append(dic)
    data['result'] = True
    data['data'] = datas
    
    return HttpResponse(json.dumps(data))

@csrf_exempt
@gzip_page
def Category_init(request):
    data = {}
    
    return HttpResponse(json.dumps(data))
    