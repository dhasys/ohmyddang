# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.db.models import Sum
from django.contrib.auth.models import *
from cms.models import *
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from wand.image import Image
from common.common import *
from django.core.files.base import ContentFile
from datetime import timedelta
import datetime
import hashlib
import math
import logging

logger = logging.getLogger(__name__)

_BILL_TYPE_POINT = 1
_BILL_TYPE_SUBSCRIPTION = 2

_EXPENSE_TYPE_BASIC = 0
_EXPENSE_TYPE_PHONE = 1
_EXPENSE_TYPE_CREDIT = 2
_EXPENSE_TYPE_ACCOUNT = 3

_DISCOUNT_TYPE_PRICE = 0
_DISCOUNT_TYPE_RATE = 1

_PUSH_RESERVED = 0
_PUSH_SENT = 1

_COUPON_POINT = 50

# 발행중 1 , 발행대기 2 , 발행중지 3, 기존상품 4, 발행대기중이나, 이미발행한상태 22
_STATUS_PUBLISH = 1
_STATUS_WAIT = 2
_STATUS_STOP = 3
_STATUS_EXPIRED = 4
_STATUS_PUBLSH_OR_WAIT = 22


@receiver(user_logged_in)
def member_login(sender, request, user, **kwargs):
    return


@login_required
def store_login(request, s_id):
    if int(s_id) > 0:
        if request.user.is_staff is False:
            return HttpResponseRedirect('/')
        admin_user = request.user
        store_user = Store.objects.get(id=s_id).user
        store_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, store_user)
        request.session['admin_login'] = admin_user
    elif int(s_id) == 0:
        if 'admin_login' in request.session:
            admin_user = request.session['admin_login']
            admin_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, admin_user)
            request.session['admin_login'] = None

    return HttpResponseRedirect('/')


@login_required
def main(request):
    url = '/store/register/'
    #print 'main'
    #print request.user
    #url = '/store/list'
    
    if request.user.is_staff == True:
        url = '/store/list'
    else:
        store = Store.objects.filter(user=request.user)
        if len(store) == 1:
            print '2'
            store = store[0]
            url = '/store/detail/%d' % store.id
            if store.activate_flag is False:
                return HttpResponse(u'<script>alert("가입 승인 대기중입니다.");location.href="/logout/";</script>')
    return HttpResponseRedirect(url)
    #return

def store_register(request, s_id=0):
    #logger.error('Something went wrong!')
    if request.user.is_staff is False:
        if s_id > 0:
            print s_id
            store = Store.objects.filter(id=s_id, visible_flag=True)
            if len(store) == 0:
                return HttpResponseRedirect('/')
            else:
                store = store[0]
            if validate_user(request.user, s_id) is False:
                return HttpResponseRedirect('/store/modify/' + str(Store.objects.filter(user=request.user)[0].id))
        else:
            if request.user.is_authenticated():
                return HttpResponseRedirect('/store/detail/' + str(Store.objects.filter(user=request.user)[0].id))

    variables = RequestContext(request)
    dictionary = {}

    mode = 'register'
    get_times(dictionary)
    pictures = []

    if s_id > 0:
        mode = 'modify'
        store = Store.objects.get(id=s_id)
        dictionary['store'] = store
        dictionary['s_id'] = s_id
        pictures = store.pictures.all()
    else:
        dictionary['s_id'] = 0

    arr = []
    for i in range(10):
        if i < len(pictures):
            arr.append(pictures[i])
        else:
            arr.append(None)
    dictionary['pictures'] = arr
    dictionary['mode'] = mode
    
    
    print s_id

    return render_to_response('store_register.html', dictionary, variables)

@api_decorator
def store_register_save_1(request, data):
    is_register_success = False
   
   #result = get_store_detail_info(data);
   #if result['reuslt'] is False:
    store_id = data['store_id']
    
    # 쿠폰 포인트의 data디폴트값이 정해져 있어야함.
    
    
    user = User.objects.filter(username=store_id)
    if len(user) > 0:
        return {'result': False, 'msg': "등록된 ID 입니다"}
        
    user = User()
    user.username = data['store_id']
    user.set_password(data['password'])
    user.email = data['email']
    user.is_staff = False
    user.save()
    #가입시에 등록하면 수정 불가능한 내용들.
    store = Store()
    store.store_name = data['store_name']
    store.president_name = data['president_name']
    store.business_number = data['business_number']
    store.user = user
    store.search = data['store_name'].strip().replace(" ", "") + '|' + data['president_name'].strip().replace(" ", "")
    store.store_type = data['store_type']
    is_register_success = True;
    store.save()
    
    if is_register_success:
        result = {'result': True, 'msg': "사용가능", 'id': store.id}
    else:
        result = {'result': False, 'msg': "사용불가능"}
    return result

    #return {'result': False, 'msg': "사용불가능"}

@api_decorator
def store_register_save(request, data=None):
    is_register_success = False
    
      
    if request.method == "POST":
        store = None
        user = None
        req = request.POST
      
        if req['s_id'] == '':
            s_id = 0
        else:
            s_id = int(req['s_id'])
        
      
        if s_id > 0: 
            store = Store.objects.get(id=s_id)
            user = User.objects.get(id=store.user.id)
            if req['password'] != '':
                user.set_password(req['password'])
                user.save()
            if req['email'] != '':
                user.email = req['email']
                user.save()
    
        else:    
            
            user = User()
            user.username = req['store_id']
            user.set_password(req['password'])
            user.email = req['email']
            user.is_staff = False
            user.save()
            #가입시에 등록하면 수정 불가능한 내용들.
            store = Store()
            store.store_name = req['store_name']
            store.president_name = req['president_name']
            store.business_number = req['business_number']
            store.user = user
            store.search = req['store_name'].strip().replace(" ", "") + '|' + req['president_name'].strip().replace(" ", "")
            if 'store_type' in req:
                store.store_type = req['store_type']
            is_register_success = True;
                        

    store.save()

        
    if len(req['del_pic']) > 0:
        arr_pic = req['del_pic'].split(',')
        pictures = store.pictures.all()
        arr_pic = arr_pic[1:]
        arr_pic.sort()
        arr_pic.reverse()
        for item in arr_pic:
            store.pictures.remove(pictures[int(item) - 1])
            store.save()

    if req['delete_pi'] == '1':
        store.prime_image = None
        store.save()

    for file_str in request.FILES:
        if 'prime_image' == file_str:
            pic = picture_save(request_file=request.FILES['prime_image'], original_file_size=(184, 184), original_file_type='gif', compress_file_type='gif', compress_file_size=(65, 65))
            store.prime_image = pic
            store.save()
        else:
            pic = picture_save(request_file=request.FILES[file_str], compress_file_size=(140, 140))
            store.pictures.add(pic)
            store.save()


    if data is None:
        if is_register_success:
            return HttpResponseRedirect("/member/list")
        else:
            # 일반회원을 등록할때 ID 나 별명이 중복되어있을 경우에 예외처리가 되어야 함.
            # "아이디 와 닉네임 중복되어서 멤버 가입되지 않음"
            return HttpResponseRedirect("/member/list")
    else:
        if is_register_success:
            result = {'result': True, 'msg': "사용가능", 'id': store.id}
        else:
            result = {'result': False, 'msg': "사용불가능"}

        return result



def picture_save(request_file, original_file_size=(0, 0), original_file_type='jpeg', compress_file_size=(0, 0), compress_file_type='jpeg'):
    pic = Picture()
    pic.save()

    original_image = Image(blob=request_file.read())
    compress_image = original_image.clone()

    original_image.format = original_file_type
    compress_image.format = compress_file_type
    w, h = original_image.size

    original_width = w
    compress_width = w
    original_height = h
    compress_height = h

    if original_file_size[0] > 0:
        original_width = original_file_size[0]
    if original_file_size[1] > 0:
        original_height = original_file_size[1]

    if compress_file_size[0] > 0:
        compress_width = compress_file_size[0]
    if compress_file_size[1] > 0:
        compress_height = compress_file_size[1]

    original_image.resize(original_width, original_height)
    original_image.compression_quality = 60

    compress_image.resize(compress_width, compress_height)
    compress_image.compression_quality = 60

    pic.original_image.save(str(pic.id) + u'_o.' + original_file_type, ContentFile(original_image.make_blob()))
    pic.compress_image.save(str(pic.id) + u'_c.' + compress_file_type, ContentFile(compress_image.make_blob()))

    return pic


@login_required
def store_detail(request, s_id):
    if validate_user(request.user, s_id) is False:
        return HttpResponseRedirect('/')

    variables = RequestContext(request)
    dictionary = {}
    store = Store.objects.filter(id=s_id, visible_flag=True)
    if len(store) == 0:
        return HttpResponseRedirect('/logout')
    else:
        store = store[0]
        if store.activate_flag == True:
            today = datetime.datetime.today()
            subscription_mybill = MyBill.objects.filter(store=store, useable=True, activated_date__lte=today, expired_date__gte=today)
            if len(subscription_mybill) == 1:
                dictionary['subscription_mybill'] = True
            mybill = MyBill.objects.filter(store=store, useable=True, activated_date=None, expired_date=None)
            if len(mybill) > 0:
                sum_point = mybill.aggregate(Sum('point'))['point__sum']
                use_point = MyCoupon.objects.filter(coupon__store=store, subscription_flag=False).count() * _COUPON_POINT
                dictionary['point'] = sum_point - use_point

    dictionary['store'] = store
    dictionary['store_user'] = User.objects.get(store=store)
    dictionary['sum_point'] = point_check(store)
    return render_to_response('store_detail.html', dictionary, variables)


@staff_member_required
@login_required
def store_register_activate(request, s_id):
    store = Store.objects.get(id=s_id)
    store.activate_flag = True
    store.save()
    # 가입시 기본포인트 제공.
    bill = MyBill()
    bill.store = store
    bill.point = 5000
    bill.expense_type = _EXPENSE_TYPE_BASIC
    bill.expense_price = 0
    bill.save()

    return HttpResponseRedirect('/store/list')


def set_store_search():
    # store 가맹점명과 대표자명을 일괄적으로 search 필드에 저장.
    stores = Store.objects.all()
    for store in stores:
        store_text = store.store_name.strip().replace(" ", "")
        manager_text = store.manager_name.strip().replace(" ", "")
        store.search = store_text + '|' + manager_text
        store.save()


@staff_member_required
@login_required
def store_list(request, page_number=1):
    
    total_count = Store.objects.all().order_by("-id").count()
    dic = get_page_list(request, page_number, total_count=total_count)
    documents = Store.objects.filter(visible_flag=True).order_by('-id')[int(dic['start_offset']):int(dic['end_offset'])]
    req = request.POST
    if 'search_text' in req:
        if req['search_text'] != '':
            search = req['search_text'].strip().replace(" ", "")
            documents = Store.objects.filter(visible_flag=True, search__contains=search).order_by('-id')

    variables = RequestContext(request)
    documents = documents.values()
    for i, document in enumerate(documents):
        document['coupon_count'] = Coupon.objects.filter(store=Store.objects.get(id=document['id']), visible_flag=True).count()

    dic.update({"documents": documents})
    variables = RequestContext(request, dic)

    return render_to_response('store_list.html', dic, variables)
    #return render_to_response('store_list.html')


# @staff_member_required
@store_login_required
@login_required
def coupon_register(request, c_id=0):
    variables = RequestContext(request)
    mode = 'register'
    if c_id > 0:
        mode = 'modify'

    dictionary = {}
    get_times(dictionary)
    get_url(request, dictionary)

    if mode == 'modify':
        cp = Coupon.objects.get(id=c_id)
        today = datetime.datetime.today()

        if cp.activated_date_time <= today and today < cp.expired_date_time:
            return HttpResponseRedirect('/coupon/detail/' + c_id)
        dictionary['coupon'] = cp
        dictionary['c_id'] = c_id
        if today_check(cp):
            dictionary['radio'] = 1
        else:
            dictionary['radio'] = 2
    else:
        dictionary['c_id'] = 0
    dictionary['mode'] = mode
    #weeks = [u'월', u'화', u'수', u'목', u'금', u'토', u'일']
    #dictionary['weeks'] = weeks
    store = Store.objects.get(user=request.user)
    dictionary['store'] = store
    results = get_coupon_extra_point(store.id)
    dictionary['subscription'] = results['subscription']
    dictionary['available_cnt'] = results['available_cnt']

    return render_to_response('coupon_register.html', dictionary, variables)
    # return render_to_response('common.js', dictionary, variables)


def today_check(coupon):
    result = False
    today = datetime.datetime.today()
    act_y = coupon.activated_date_time.year
    act_m = coupon.activated_date_time.month
    act_d = coupon.activated_date_time.day
    exp_y = coupon.expired_date_time.year
    exp_m = coupon.expired_date_time.month
    exp_d = coupon.expired_date_time.day
    if today.year == act_y and today.month == act_m and today.day == act_d:
        if today.year == exp_y and today.month == exp_m and today.day == exp_d:
            result = True
    return result



@store_login_required
@api_decorator
def coupon_register_save(request):
    dictionary = {}
    if request.method == "POST":
        req = request.POST
        today = datetime.datetime.now()
        c_id = req['c_id']

        if c_id == '0':
            dictionary['mode'] = 'register'
            coupon = Coupon()
        else:
            dictionary['mode'] = 'modify'
            dictionary['c_id'] = c_id
            coupon = Coupon.objects.get(id=c_id)
            status = get_coupon_status(coupon)
            if status == u"기존상품":
                coupon.visible_flag = False
                coupon.save()
                new_coupon = Coupon()
                new_coupon.image = coupon.image
                coupon = new_coupon

        # 앱에서 호출되는 api 유무 체크.
        if 'type' in req:
            store = Store.objects.get(id=req['s_id'])
        else:
            store = Store.objects.get(user=request.user)

        #현재로그인한 가맹점의 store 를 찾아서 넣어줌.
        coupon.store = store
        coupon.name = req['coupon_name']
        coupon.search = req['coupon_name'].strip().replace(" ", "")
        coupon.description = req['description']
        coupon.count = int(req['coupon_count'])

        if int(req['discount_type']) == _DISCOUNT_TYPE_PRICE:
            coupon.original_price = int(req['original_price'])
            coupon.discount_price = int(req['discount_price'])
            coupon.discount_percentage = 0
        elif int(req['discount_type']) == _DISCOUNT_TYPE_RATE:
            coupon.discount_percentage = int(req['discount_percentage'])
            coupon.original_price = 0
            coupon.discount_price = 0

        if 'main_category' in req:
            coupon.item_type = req['main_category']
            coupon.item_sub_type = req['sub_category']
        
        #coupon.activated_date_time = datetime.datetime.today()
        #coupon.expired_date_time = datetime.datetime.today()

        #my_bill = MyBill.objects.filter(store=store, activated_date__lte=today, expired_date__gte=today, useable=True)
        my_bill = MyBill.objects.filter(store=store, useable=True)
        
        if len(my_bill) == 1:
            coupon.subscription_flag = True
        else:
            coupon.subscription_flag = False
            
        
        coupon.save()

        for i in range(1,3):
            strTemp1 = 'option_name_' + str(i)
            strTemp2 = 'option_count_' + str(i)
            
            if strTemp1 in req:
                option = Option()
                option.option_name = req[strTemp1]
                option.option_count = req[strTemp2]
                option.save()
                
                coupon.options.add(option)
            
            coupon.save()
                
                
        
        
        #if 'time_type' in req:
        #    if req['time_type'] == '1':
        #        coupon.activated_date_time = datetime.datetime(int(req['start_y']), int(req['start_m']), int(req['start_d']), int(req['start_h']), int(req['start_minute']))
        #        coupon.expired_date_time = datetime.datetime(int(req['end_y']), int(req['end_m']), int(req['end_d']), int(req['end_h']), int(req['end_minute']))
        #        week_list = request.POST.getlist("week")
        #        tmp = ''
        #        if 'type' in req:
        #            for week in week_list:
        #                week = week[1:][:-1]
        #            tmp = week
        #        else:
        #            for w in week_list:
        #                tmp += w + ','
        #            tmp = tmp[:-1]
        #        coupon.weeks = tmp
        #    else:
        #        coupon.activated_date_time = datetime.datetime(today.year, today.month, today.day, int(req['start_h']), int(req['start_minute']))
        #        coupon.expired_date_time = datetime.datetime(today.year, today.month, today.day, int(req['end_h']), int(req['end_minute']))
        #        coupon.weeks = today.weekday()

        if req['del_pic'] == '1':
            coupon.image = None
            coupon.save()

        #if 'picture' in request.FILES:
        #     pic = picture_save(request.FILES['picture'], original_file_size=(720, 450), compress_file_size=(242, 152))
        #    coupon.image = pic
        
        dic = {}
        dic['reuslt'] = True
        
        for file_str in request.FILES:
            if 'picture' == file_str:
                pic = picture_save(request.FILES['picture'], original_file_size=(720, 450), compress_file_size=(242, 152))
                coupon.image = pic
                dic['pic'] = True 
                store.save()
            else:
                pic = picture_save(request_file=request.FILES[file_str], compress_file_size=(242, 152))
                coupon.pictures.add(pic)
                coupon.save()
                dic['reuslt'] = True
                dic['pic1'] = pic.compress_image.url
                
            
        coupon.save()

    if 'type' in req:
        return dic
    else:
        return HttpResponseRedirect('/coupon/list/publish')


def get_coupon(user, c_id):
    cp = Coupon.objects.filter(store__user=user, id=c_id, visible_flag=True)
    if len(cp) == 0:
        return None
    else:
        return cp[0]


@store_login_required
@login_required
def coupon_toggle(request, c_id=0):
    cp = get_coupon(request.user, c_id)
    if cp == None:
        return HttpResponseRedirect('/coupon/list/publish')

    cp.publish_flag = not cp.publish_flag
    cp.save()

    return HttpResponseRedirect('/coupon/list/publishstop')


@store_login_required
@login_required
def coupon_detail(request, c_id=0):
    variables = RequestContext(request)
    dictionary = {}
    today = datetime.datetime.today()

    cp = get_coupon(request.user, c_id)
    if cp == None:
        return HttpResponseRedirect('/coupon/list/publish')

    dictionary['coupon'] = cp
    status = get_coupon_status(cp)
    if status == u"발행중":
        dictionary['coupon_status'] = _STATUS_PUBLISH
    #elif status == u"발행대기":
    #    dictionary['coupon_status'] = _STATUS_WAIT
    #    if cp.activated_date_time <= today and today < cp.expired_date_time:
            # 발행대기리스트에 있지만 이미 발행중인상품.(예를들어, 요일발행같은상품의 경우 --> 수정할수없음.)
    #        dictionary['coupon_status'] = _STATUS_PUBLSH_OR_WAIT
    elif status == u"기존상품":
        dictionary['coupon_status'] = _STATUS_EXPIRED
    elif status == u"발행중지":
        dictionary['coupon_status'] = _STATUS_STOP

    #weeks = [u'월', u'화', u'수', u'목', u'금', u'토', u'일']
    #tmp_list = cp.weeks.split(u',')
    #weeks_str = ''
    #for t in tmp_list:
    #    weeks_str += weeks[int(t)] + u','

    #dictionary['weeks'] = weeks_str[:-1]

    return render_to_response('coupon_detail.html', dictionary, variables)


def set_coupon_search():
    # db에 일괄적으로 search 필드 추가함.
    coupons = Coupon.objects.all()
    for coupon in coupons:
        coupon.search = coupon.name.strip().replace(" ", "")
        coupon.save()


def search_coupon_list(documents):
    arr_coupon_status = []
    for cp in documents:
        arr_coupon_status.append(get_coupon_status(cp))
    return arr_coupon_status


@store_login_required
@login_required
def coupon_list(request, c_type, page_number=1):
    store = Store.objects.filter(user=request.user)
    if len(store) == 0:
        return HttpResponseRedirect('/')
    else:
        store = store[0]
    # set_coupon_search()
    arr_coupon_status = []
    if request.POST:
        req = request.POST
        search = req['search_text']
        search = search.strip().replace(" ", "")
        request.session['search_text'] = search
        if search == "":
            return HttpResponseRedirect('/coupon/list/publish')
        else:
            c_type = 'search'

    total_count = 0
    dic = None
    documents = None

    if c_type == 'search':
        search = request.session['search_text']
        total_count = Coupon.objects.filter(store=store, visible_flag=True, search__contains=search).order_by('-id').count()
        dic = get_page_list(request, page_number, total_count=total_count)
        documents = Coupon.objects.filter(store=store, visible_flag=True, search__contains=search).order_by('-id')[int(dic['start_offset']):int(dic['end_offset'])]
        # documents = Coupon.objects.filter(store=store, visible_flag=True, search__contains=search).order_by('-id')
        if len(documents) > 0:
            # c_type = 'search'
            arr_coupon_status = search_coupon_list(documents)

    tab = {
        'registerwait': 'off',
        'publishwait': 'off',
        'publish': 'off',
        'all': 'off',
        'publishstop': 'off',
    }
    tab[c_type] = 'on'

    # 기존상품 등록, 발행중지, 발행대기, 발행중.
    today = datetime.datetime.today()
    #today_week = today.weekday()
    st = Store.objects.filter(user=request.user)
    cp = Coupon.objects.filter(store=st, visible_flag=True).order_by('-regdate')
    
    if c_type == 'publish':
        #documents = cp.filter(activated_date_time__lte=today, expired_date_time__gt=today, publish_flag=True)
        print '1'
        documents = cp.filter(publish_flag=True)
        
        #documents = documents.filter(weeks__contains=today_week)
        arr_id = []
        for coupon in documents:
            #if check_coupon_time(coupon):
                # 현재시간안에 있는쿠폰만 추려냄.
                arr_id.append(coupon.id)
        documents = documents.filter(pk__in=arr_id)
        total_count = documents.filter(pk__in=arr_id).count()
        dic = get_page_list(request, page_number, total_count=total_count)
        #documents = documents.filter(pk__in=arr_id)[int(dic['start_offset']):int(dic['end_offset'])]

    elif c_type == 'publishstop':
        # 발행중지된 쿠폰.
        total_count = cp.filter(publish_flag=False).count()
        dic = get_page_list(request, page_number, total_count=total_count)
        documents = cp.filter(publish_flag=False)[int(dic['start_offset']):int(dic['end_offset'])]
    else:
        if c_type != 'search':
            total_count = cp.count()
            dic = get_page_list(request, page_number, total_count=total_count)
            documents = cp[int(dic['start_offset']):int(dic['end_offset'])]
            # documents = cp

    arr_image = []
    arr_down_coupon_count = []
    arr_useable_coupon_count = []

    for document in documents:
        image_url = "/static/img/top_logo.png"
        down_cnt = MyCoupon.objects.filter(coupon=document).count()
        arr_down_coupon_count.append(down_cnt)
        arr_useable_coupon_count.append(document.count - down_cnt)
        if document.image:
            image_url = document.image.original_image.url
        arr_image.append(image_url)

    # convert class to dictionary
    documents = documents.values()
    for i, document in enumerate(documents):
        document['image_url'] = arr_image[i]
        document['down_coupon_count'] = arr_down_coupon_count[i]
        document['useable_coupon_count'] = arr_useable_coupon_count[i]
        if c_type == 'search':
            document['coupon_status'] = arr_coupon_status[i]

    #set_week_list(documents)

    # dic = get_obj_list(request, page_number, documents)

    dic['tab'] = tab
    dic['c_type'] = c_type
    dic.update({"documents": documents})
    variables = RequestContext(request, dic)
    return render_to_response('coupon_list.html', variables)


def set_week_list(documents):
    weeks = [['0', u'월'], ['1', u'화'], ['2', u'수'], ['3', u'목'], ['4', u'금'], ['5', u'토'], ['6', u'일']]

    for document in documents:
        raw_week = document['weeks']
        for week in weeks:
            raw_week = raw_week.replace(week[0], week[1])
        document['new_week'] = raw_week


@login_required
def notice_register(request, n_id=0):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/notice/list')
    variables = RequestContext(request)
    dictionary = {}
    if n_id > 0:
        dictionary['n_obj'] = Notice.objects.get(id=n_id)

    return render_to_response('notice_register.html', dictionary, variables)


@login_required
def notice_register_save(request):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/notice/list')

    if request.method == "POST":
        req = request.POST
        n_id = req['n_id']
        notice = None
        if n_id > '0':
            notice = Notice.objects.get(id=n_id)
        else:
            notice = Notice()

        notice.title = req['title']
        notice.contents = req['contents']
        if 'display_flag' in req:
            notice.display_flag = True
        else:
            notice.display_flag = False
        notice.save()

    return HttpResponseRedirect("/notice/list")


@login_required
def notice_list(request, page_number=1):
    variables = RequestContext(request)
    total_count = Notice.objects.all().order_by("-id").count()
    dic = get_page_list(request, page_number, total_count=total_count)
    documents = Notice.objects.all().order_by("-regdate")[int(dic['start_offset']):int(dic['end_offset'])]
    dic.update({"documents": documents})

    return render_to_response('notice_list.html', dic, variables)


@login_required
def notice_detail(request, n_id):
    variables = RequestContext(request)
    dictionary = {}
    notice = get_notice(request.user, n_id)
    if notice is None:
        return HttpResponseRedirect('/notice/list')
    dictionary['notice'] = notice

    return render_to_response('notice_detail.html', dictionary, variables)


def get_board(user, b_id):
    if user.is_staff is True:
        board = Board.objects.filter(id=b_id)
    else:
        board = Board.objects.filter(store__user=user, id=b_id)
    if len(board) == 0:
        return None
    else:
        return board[0]


@store_login_required
@login_required
def board_register(request, b_id=0):
    if b_id > 0:
        board = get_board(request.user, b_id)
        if board == None:
            return HttpResponseRedirect('/board/list')

    variables = RequestContext(request)
    dictionary = {}
    if b_id > 0:
        dictionary['b_obj'] = Board.objects.get(id=b_id)

    return render_to_response('board_register.html', dictionary, variables)


@store_login_required
@login_required
def board_register_save(request):
    if request.method == "POST":
        req = request.POST
        b_id = req['b_id']
        board = None
        if b_id > '0':
            board = Board.objects.get(id=b_id)
        else:
            board = Board()

        board.store = Store.objects.get(user=request.user)
        board.title = req['title']
        board.contents = req['contents']
        board.save()

    return HttpResponseRedirect("/board/list")


@login_required
def board_list(request, page_number=1):
    # board = get_board(request.user, b_id)
    # if board == None:
    #     return HttpResponseRedirect('/board/list')
    variables = RequestContext(request)
    documents = None
    dic = None

    if request.user.is_staff == True:
        total_count = Board.objects.all().count()
        dic = get_page_list(request, page_number, total_count=total_count)
        documents = Board.objects.all().order_by("-id")[int(dic['start_offset']):int(dic['end_offset'])]
    else:
        st = Store.objects.filter(user=request.user)
        total_count = Board.objects.filter(store=st).count()
        dic = get_page_list(request, page_number, total_count=total_count)
        documents = Board.objects.filter(store=st).order_by("-regdate")[int(dic['start_offset']):int(dic['end_offset'])]

    dic.update({"documents": documents})

    return render_to_response('board_list.html', dic, variables)


@login_required
def board_detail(request, b_id=0):
    # if request.user.is_staff is False:
    board = get_board(request.user, b_id)
    if board is None:
        return HttpResponseRedirect('/board/list')

    dictionary = {}
    # board = Board.objects.get(id=b_id)
    br = BoardReply.objects.filter(board=board)
    if len(br) == 1:
        dictionary['board_reply'] = br[0]
    dictionary['board'] = board

    return render_to_response('board_detail.html', RequestContext(request, dictionary))


def board_reply(request, b_id):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    dictionary = {}
    board = Board.objects.get(id=b_id)
    if board.reply_flag == True:
        #이미 답변이 달린상황이므로 댓글을 수정하려는것임
        dictionary['br_obj'] = BoardReply.objects.get(board=board)
    #else:
    #댓글을 새로 달려고 하는것이다. 아직 플래그가 false

    dictionary['b_id'] = b_id
    dictionary['b_obj'] = board
    dictionary['store'] = Store.objects.get(id=board.store.id)
    return render_to_response('board_reply.html', RequestContext(request, dictionary))


def board_reply_save(request):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        req = request.POST
        br = None
        board = Board.objects.get(id=req['b_id'])
        br = BoardReply.objects.filter(board=board)
        if len(br) > 0:
            br = br[0]
        else:
            br = BoardReply()

        board.reply_flag = True
        board.save()
        br.board = board
        br.contents = req['reply_contents']
        br.save()
        url = '/board/detail/' + req['b_id']
    return HttpResponseRedirect(url)


@staff_member_required
@login_required
def member_register(request, m_id=0):
    variables = RequestContext(request)
    dictionary = {}
    get_times(dictionary)
   
    if m_id > 0:
        member = Member.objects.filter(id=m_id)
        if len(member) == 0:
            return HttpResponseRedirect('/')
        else:
            member = member[0]
            dictionary['member'] = member
            if member.is_fake_id is True:
                dictionary['coupon_down_cnt'] = member.fake_download_count
                dictionary['coupon_used_cnt'] = member.fake_coupon_used_count
            else:
                dictionary['coupon_down_cnt'] = MyCoupon.objects.filter(member=member).count()
                dictionary['coupon_used_cnt'] = MyCoupon.objects.filter(member=member, useable=True).count()

    return render_to_response('member_register.html', dictionary, variables)


@api_decorator
def member_register_save(request, data=None):
    is_register_success = ''
   
    #if request.method == "POST":
    if data is None:
        req = request.POST
        m_id = 0
        if req['m_id'] != '':
            m_id = int(req['m_id'])
        member = None
        if m_id > 0:
            member = Member.objects.get(id=m_id)
        else:
            member = Member()
    else:
        req = data
        m_id =  0
        if 'm_id' in data:
            m_id = int(data['m_id'])

        if m_id > 0:
            member = Member.objects.get(id=data['m_id'])
        else:
            member = Member()

    if m_id > 0:
        member_update(member, req)
        is_register_success = True
    else:
        if member_login_duplicate_check(req):
            member.udid = req['member_id']
            
            val = req['member_nickname']
            if len(val) > 0:
                member.nickname = req['member_nickname']
            else:
                member.nickname = None
            member_update(member, req)
            is_register_success = True
        else:
            is_register_success = False
    
    if data is None:
        if is_register_success:
            return HttpResponseRedirect("/member/list")
        else:
            # 일반회원을 등록할때 ID 나 별명이 중복되어있을 경우에 예외처리가 되어야 함.
            # "아이디 와 닉네임 중복되어서 멤버 가입되지 않음"
            return HttpResponseRedirect("/member/list")
    else:
        if is_register_success:
            result = {'result': True, 'msg': "사용가능", 'id': member.id}
        else:
            result = {'result': False, 'msg': "사용불가능"}

        return result


def member_update(member, req):
    val = ''
    if 'bir_day' in req:
        val = req['bir_day']
    
    if len(val) > 0:
        birth_date = req['bir_day'] + req['bir_mon'] + req['bir_year']
        birth_datetime = datetime.datetime.strptime(birth_date, "%d%m%Y")
        member.birthday = birth_datetime
    else:
        member.birthday = None

    if 'member_nickname' in req:
        member.nickname = req['member_nickname']

    if 'gender' in req:
        if req['gender'] == "":
            member.gender = None
        else:
            member.gender = int(req['gender'])

    if 'member_coupon_down_count' in req:
        if len(req['member_coupon_down_count']) > 0:
            member.fake_download_count = int(req['member_coupon_down_count'])

    if 'member_coupon_use_count' in req:
        if len(req['member_coupon_use_count']) > 0:
            member.fake_coupon_used_count = int(req['member_coupon_use_count'])

    if 'is_fake' in req:
        member.is_fake_id = True

    member.save()

 # total_count = Member.objects.all().order_by("-id").count()
    # dic = get_page_list(request, page_number, total_count=total_count)
    # documents = Store.objects.filter(visible_flag=True).order_by('-id')[int(dic['start_offset']):int(dic['end_offset'])]


@login_required
def member_list(request, page_number="1"):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    variables = RequestContext(request)

    total_count = Member.objects.all().order_by("-id").count()
    dic = get_page_list(request, int(page_number), total_count=total_count)
    documents = Member.objects.all().order_by("-id")[int(dic['start_offset']):int(dic['end_offset'])]
    documents = documents.values()
    for i, document in enumerate(documents):
        if document['is_fake_id'] is True:
            document['coupon_down_cnt'] = document['fake_download_count']
            document['coupon_used_cnt'] = document['fake_coupon_used_count']
        else:
            document['coupon_down_cnt'] = MyCoupon.objects.filter(member=Member.objects.get(id=document['id'])).count()
            document['coupon_used_cnt'] = MyCoupon.objects.filter(member=Member.objects.get(id=document['id']), useable=True).count()

    dic.update({"documents": documents})

    return render_to_response('member_list.html', dic, variables)


def member_detail(request, m_id):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    variables = RequestContext(request)
    dictionary = {}
    member = Member.objects.filter(id=m_id)
    if len(member) == 0:
        return HttpResponseRedirect('/')
    member = member[0]
    if member.is_fake_id is True:
        dictionary['coupon_down_cnt'] = member.fake_download_count
        dictionary['coupon_used_cnt'] = member.fake_coupon_used_count
    else:
        dictionary['coupon_down_cnt'] = MyCoupon.objects.filter(member=member).count()
        dictionary['coupon_used_cnt'] = MyCoupon.objects.filter(member=member, useable=True).count()

    dictionary['member'] = member

    return render_to_response('member_detail.html', dictionary, variables)


@login_required
def push_register(request, p_id=0):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    variables = RequestContext(request)
    dictionary = {}
    get_times(dictionary)
    if p_id > 0:
        push = Push.objects.filter(id=p_id)
        if len(push) == 1:
            push = push[0]
            if datetime.datetime.today() < push.activated_date_time:
                dictionary['push'] = push
            else:
                return HttpResponseRedirect('/push/list')
        else:
            return HttpResponseRedirect('push/list')

    return render_to_response('push_register.html', dictionary, variables)


@login_required
def push_register_save(request):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        req = request.POST
        p_id = req['p_id']
        push = None
        if p_id > '0':
            push = Push.objects.get(id=p_id)
        else:
            push = Push()

        push.contents = req['contents']

        if req['time_type'] == '0':
            push.activated_date_time = datetime.datetime.now()
        elif req['time_type'] == '1':
            push.activated_date_time = datetime.datetime(int(req['start_y']), int(req['start_m']), int(req['start_d']), int(req['start_h']), int(req['start_minute']))
        push.save()
        push_send(push.id, 0)

    return HttpResponseRedirect("/push/list")


def push_resent(request, p_id):
    # 푸쉬 바로발송
    now = datetime.datetime.now()
    push = Push.objects.filter(id=p_id, activated_date_time__gt=now)
    if len(push) == 1:
        push = push[0]
    else:
        # 이미 발송된 push 의 경우 다시 발송 안함.
        return HttpResponseRedirect("/push/list")
    push.activated_date_time = now
    push.save()
    push_send(push.id, 0)

    return HttpResponseRedirect("/push/list")


@login_required
def push_detail(request, p_id):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    variables = RequestContext(request)
    dictionary = {}
    push = get_push(request.user, p_id)
    if push is None:
        return HttpResponseRedirect('/push/list')
    dictionary['push'] = push
    if datetime.datetime.today() < push.activated_date_time:
        dictionary['date_status'] = _PUSH_RESERVED
    else:
        dictionary['date_status'] = _PUSH_SENT

    return render_to_response('push_detail.html', dictionary, variables)


@login_required
def push_list(request, page_number=1):
    if request.user.is_staff is False:
        return HttpResponseRedirect('/')
    variables = RequestContext(request)

    total_count = Push.objects.all().order_by("-id").count()
    dic = get_page_list(request, page_number, total_count=total_count)
    documents = Push.objects.all().order_by("-id")[int(dic['start_offset']):int(dic['end_offset'])]

    today = datetime.datetime.today()
    arr_date_status = []
    for item in documents:
        if today < item.activated_date_time:
            arr_date_status.append(_PUSH_RESERVED)
        else:
            arr_date_status.append(_PUSH_SENT)

    documents = documents.values()
    for i, document in enumerate(documents):
        document['date_status'] = arr_date_status[i]

    dic.update({"documents": documents})
    return render_to_response('push_list.html', dic, variables)


@login_required
def point_register(request, p_id=0):
    variables = RequestContext(request)
    dictionary = {}
    dictionary['bill'] = Bill.objects.all().filter(visible_flag=True)

    return render_to_response('point_register.html', dictionary, variables)


@login_required
def point_register_save(request):
    if request.method == "POST":
        req = request.POST
        bill = Bill()
        bill.bill_type = int(req['point_type'])
        bill.point = int(req['point'])
        bill.price = int(req['price'])
        bill.save()

    return HttpResponseRedirect("/point/register")


@login_required
def point_list(request, page_number=1):
    variables = RequestContext(request)
    store = Store.objects.filter(user=request.user)
    is_staff = False
    if request.user.is_staff:
        total_count = MyBill.objects.all().exclude(expense_type=_EXPENSE_TYPE_BASIC).order_by("-regdate").count()
        dic = get_page_list(request, page_number, total_count=total_count)
        # 기본으로 제공하는 포인트를 제외한 모든 포인트들.
        documents = MyBill.objects.all().exclude(expense_type=_EXPENSE_TYPE_BASIC).order_by("-regdate")[int(dic['start_offset']):int(dic['end_offset'])]
        is_staff = True
    else:
        if len(store) > 0:
            store = store[0]
            total_count = MyBill.objects.filter(store=store).order_by("-regdate").count()
            dic = get_page_list(request, page_number, total_count=total_count)
            documents = MyBill.objects.filter(store=store).order_by("-regdate")[int(dic['start_offset']):int(dic['end_offset'])]

    dic.update({"documents": documents, "is_staff": is_staff})
    # dic['is_staff'] = is_staff

    return render_to_response('point_list.html', dic, variables)


def point_check(store):
    today = datetime.datetime.today()
    use_point = MyCoupon.objects.filter(coupon__store=store, subscription_flag=False).count() * _COUPON_POINT
    result = ''
    mybill = MyBill.objects.filter(store=store, useable=True)
    subscription_bill = mybill.filter(activated_date__lte=today, expired_date__gte=today)

    if len(subscription_bill) > 0:
        # 정액제 사용중.
        subscription_bill = subscription_bill.order_by('expired_date')
        act = subscription_bill[0].activated_date
        exp = subscription_bill[0].expired_date
        sum_point = mybill.aggregate(Sum('point'))['point__sum']
        subscription_point = subscription_bill.aggregate(Sum('point'))['point__sum']
        total_point = sum_point - use_point - subscription_point
        result = '정액제 (%d-%d-%d  %d:%d ~ %d-%d-%d  %d:%d), 잔여포인트 : %d p' % (act.year, act.month, act.day , act.hour, act.minute, exp.year, exp.month, exp.day, exp.hour, exp.minute, total_point)
    else:
        mybill = mybill.filter(activated_date=None, expired_date=None)
        if len(mybill) > 0:
            sum_point = mybill.aggregate(Sum('point'))['point__sum']
            total_point = sum_point - use_point
            result = '%d p' % total_point

    return result


def point_payment(request, page_number=1):
    variables = RequestContext(request)
    dic = {}
    store = Store.objects.filter(user=request.user)

    total_count = MyBill.objects.filter(store=store[0], useable=True).exclude(expense_type=_EXPENSE_TYPE_BASIC).order_by('-regdate').count()
    dic = get_page_list(request, page_number, page_size=3, total_count=total_count)
    bills = MyBill.objects.filter(store=store[0], useable=True).exclude(expense_type=_EXPENSE_TYPE_BASIC).order_by('-regdate')[int(dic['start_offset']):int(dic['end_offset'])]

    bills = Bill.objects.filter(visible_flag=True)
    if len(bills) > 0:
        if bills[0].bill_type == 1:
            dic['bill_first_contents'] = 'funing포인트상품'
        else:
            dic['bill_first_contents'] = 'funing정액제상품'
        dic['bill_first_price'] = bills[0].price
    else:
        dic['bill_first_contents'] = 'funing'
        dic['bill_first_price'] = 0

    dic['bills'] = bills
    dic['sum_point'] = point_check(store)
    dic['president_name'] = store[0].president_name
    dic.update({"documents": bills})

    return render_to_response('point_payment.html', dic, variables)


def point_payment_verify(request):
    # 검증하고, 성공시 payment-success 에서 db에 mybill 추가하기.
    req = request.POST
    mb_serial_no = req['mb_serial_no']
    tid = req['tid']
    replycode = req['replycode']
    price = req['unitprice']
    hashresult = req['hashresult']

    result = hashlib.sha256()
    result.update(b'1234!')
    result.update(replycode + tid + mb_serial_no + price + 'KRW')
    result = result.hexdigest()

    if result == hashresult:
        return point_payment_success(request)
    else:
        return point_payment_failure(request)


def point_payment_failure(request):
    dictionary = {}
    dictionary['result'] = 'fail'

    return render_to_response('point_payment_result.html', dictionary)


def point_payment_verify_success(request):
    # 처리중 로딩이 성공적으로 확인되면 '결제완료 페이지를 보여준다.'
    dictionary = {}
    dictionary['result'] = 'verify'

    return render_to_response('point_payment_result.html', dictionary)


def point_payment_success(request):
    # 성공시에 마이빌에 추가한다.
    # 추가후 처리중이라는 html 페이지 로딩해준다.
    req = request.POST
    variables = RequestContext(request)
    dictionary = {}
    if req['bill_id'] == '':
        return HttpResponseRedirect("/point/payment/failure")
    else:
        # 관리자가 등록한 포인트내역을 삭제한경우
        pt = Bill.objects.filter(id=int(req['bill_id']), visible_flag=True)
        if len(pt) != 1:
            return HttpResponseRedirect("/point/payment/failure")
        else:
            pt = pt[0]

    my_bill = MyBill()
    store = Store.objects.get(user=request.user)
    my_bill.store = store
    my_bill.point = pt.point
    if pt.bill_type == _BILL_TYPE_SUBSCRIPTION:
        today = datetime.datetime.today()
        delta = timedelta(days=int(pt.point))
        exp = today + delta
        act = today

        # 만료일이 오늘보다 크거나 같을때 만료일을 기준으로 30일간 계산해줘야함.(오늘보다 이전이라면 , 오늘을 기준을 더해줌.)
        pre_mybill = MyBill.objects.filter(store=store, expired_date__gte=today, useable=True)
        if len(pre_mybill) > 0:
            last_mybill = pre_mybill.order_by('-expired_date')
            act = last_mybill[0].expired_date + timedelta(days=1)
            exp = act + delta

        my_bill.activated_date = act
        my_bill.expired_date = exp

    pay_type = req['paymethod']
    if pay_type == '801':
        my_bill.expense_type = _EXPENSE_TYPE_PHONE
    elif pay_type == 'card' or pay_type == '101' or pay_type == '100':
        my_bill.expense_type = _EXPENSE_TYPE_CREDIT
    elif pay_type == '4':
        my_bill.expense_type = _EXPENSE_TYPE_ACCOUNT
    my_bill.expense_price = pt.price
    my_bill.tid = req['tid']
    my_bill.save()

    dictionary['tid'] = req['tid']
    dictionary['result'] = 'success'

    return render_to_response('point_payment_result.html', dictionary, variables)


@store_login_required
@login_required
def review_register(request, r_id=0):
    variables = RequestContext(request)
    dictionary = {}
    if r_id > 0:
        sr = StoreReview.objects.filter(id=r_id)
        if len(sr) == 0:
            return HttpResponseRedirect('/review/list')
        else:
            sr = sr[0]
        if request.user != sr.store.user:
            return HttpResponseRedirect('/review/list')

        dictionary['review'] = sr

    return render_to_response('review_register.html', dictionary, variables)


@store_login_required
@login_required
def review_register_save(request):
    if request.method == "POST":
        req = request.POST
        r_id = req['r_id']

        store = Store.objects.filter(user=request.user)
        if len(store) == 0:
            return HttpResponse(u'<script>alert("가맹점으로 로그인 후 이용 바랍니다.");location.href="/";</script>')
        else:
            store = store[0]

        review = None
        if r_id > '0':
            review = StoreReview.objects.filter(id=int(r_id))
            if len(review) == 0:
                HttpResponseRedirect('/review/list')
            else:
                review = review[0]
            if request.user != store.user:
                HttpResponseRedirect('/review/list')
        else:
            review = StoreReview()

        review.store = store
        review.name = req['member_name']
        review.contents = req['contents']
        review.save()

    return HttpResponseRedirect("/review/list")


@store_login_required
@login_required
def review_detail(request, r_id):
    if r_id > 0:
        sr = StoreReview.objects.filter(id=r_id)
        if len(sr) == 0:
            return HttpResponseRedirect('/review/list')
        else:
            sr = sr[0]
        if request.user != sr.store.user:
            return HttpResponseRedirect('/review/list')

    variables = RequestContext(request)
    dictionary = {}
    dictionary['review'] = sr

    return render_to_response('review_detail.html', dictionary, variables)


@store_login_required
@login_required
def review_list(request, page_number=1):
    variables = RequestContext(request)
    st = Store.objects.get(user=request.user)
    total_count = StoreReview.objects.filter(store=st).order_by('-regdate').count()
    dic = get_page_list(request, page_number, total_count=total_count)
    documents = StoreReview.objects.filter(store=st).order_by('-regdate')[int(dic['start_offset']):int(dic['end_offset'])]
    dic.update({"documents": documents})
    return render_to_response('review_list.html', dic, variables)


@login_required
def statistics(request, tab_type='months'):
    req = request.POST
    variables = RequestContext(request)
    store = Store.objects.filter(user=request.user, visible_flag=True)
    store_login_flag = False

    if len(store) > 0:
        store = store[0]
        store_login_flag = True

    tab = {
        'all': 'off',
        'years': 'off',
        'months': 'off',
        'days': 'off',
    }
    tab[tab_type] = 'on'

    dictionary = {}
    dictionary['tab'] = tab
    visit = None
    today = datetime.datetime.today()

    if tab_type == 'all':
        if store_login_flag is True:
            visit = Visit.objects.filter(store=store, member__visible_flag=True)
            down_coupon = MyCoupon.objects.filter(coupon__store=store, member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(coupon__store=store, useable=False, member__visible_flag=True)
        else:
            visit = Visit.objects.all().filter(member__visible_flag=True)
            down_coupon = MyCoupon.objects.all().filter(member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(useable=False, member__visible_flag=True)
        get_pie_chart(visit, down_coupon, use_coupon, dictionary)

    if tab_type == 'years' or tab_type == 'months':
        if 'years' in req:
            sel_year = int(req['years'])
        else:
            sel_year = today.year

        dictionary['sel_year'] = sel_year
        if store_login_flag is True:
            visit = Visit.objects.filter(store=store, visit_date__year=sel_year, member__visible_flag=True)
            down_coupon = MyCoupon.objects.filter(coupon__store=store, regdate__year=sel_year, member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(coupon__store=store, usedate__year=sel_year, useable=False, member__visible_flag=True)
        else:
            visit = Visit.objects.filter(visit_date__year=sel_year, member__visible_flag=True)
            down_coupon = MyCoupon.objects.filter(regdate__year=sel_year, member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(usedate__year=sel_year, useable=False, member__visible_flag=True)

        if tab_type == 'years':
            get_pie_chart(visit, down_coupon, use_coupon, dictionary)
        elif tab_type == 'months':
            get_column_chart(visit, down_coupon, use_coupon, dictionary)

    if tab_type == 'days':
        if 'days' in req:
            sel_year = int(req['years'])
            sel_month = int(req['months'])
            sel_day = int(req['days'])
        else:
            sel_year = today.year
            sel_month = today.month
            sel_day = today.day

        dictionary['sel_year'] = sel_year
        dictionary['sel_month'] = '%02d' % sel_month
        dictionary['sel_day'] = '%02d' % sel_day

        if store_login_flag is True:
            visit = Visit.objects.filter(store=store, visit_date__year=sel_year, visit_date__month=sel_month, visit_date__day=sel_day, member__visible_flag=True)
            down_coupon = MyCoupon.objects.filter(coupon__store=store, regdate__year=sel_year, regdate__month=sel_month, regdate__day=sel_day, member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(coupon__store=store, usedate__year=sel_year, usedate__month=sel_month, usedate__day=sel_day, useable=False, member__visible_flag=True)
        else:
            visit = Visit.objects.filter(visit_date__year=sel_year, visit_date__month=sel_month, visit_date__day=sel_day, member__visible_flag=True)
            down_coupon = MyCoupon.objects.filter(regdate__year=sel_year, regdate__month=sel_month, regdate__day=sel_day, member__visible_flag=True)
            use_coupon = MyCoupon.objects.filter(usedate__year=sel_year, usedate__month=sel_month, usedate__day=sel_day, useable=False, member__visible_flag=True)

        get_pie_chart(visit, down_coupon, use_coupon, dictionary)

    get_times(dictionary)

    return render_to_response('statistics.html', dictionary, variables)


def get_pie_chart(visit, down_coupon, use_coupon, dictionary):
    set_pie_chart_data(visit, dictionary, 'visit')
    set_pie_chart_data(down_coupon, dictionary, 'coupon_down')
    set_pie_chart_data(use_coupon, dictionary, 'coupon_use')


def set_pie_chart_data(data, dictionary, data_type, type='year'):
    data_count = data.count()
    woman = data.filter(member__gender=True).count()
    man = data.filter(member__gender=False).count()
    etc = data_count - woman - man

    if data_count == 0:
        dictionary[data_type + '_gender'] = 0
    else:
        dictionary[data_type + '_gender'] = 1

    gender_arr = [["'성별'", "'값'"], ["'남성'", man], ["'여성'", woman], ["'기타'", etc]]

    today = datetime.datetime.today()
    ages = [0, 0, 0, 0, 0, 0]
    for tmp in data:
        if tmp.member.birthday:
            age_tmp = int(math.floor((today.year - tmp.member.birthday.year + 1) / 10))
            if age_tmp >= 5:
                ages[4] += 1
            elif age_tmp == 0:
                ages[0] += 1
            else:
                ages[age_tmp - 1] += 1
        else:
            #나이를 알수없을때 기타에 카운트.
            ages[5] += 1
    age_arr = [["'나이'", "'명수'"], ["'10대이하'", ages[0]], ["'20대'", ages[1]], ["'30대'", ages[2]], ["'40대'", ages[3]], ["'50대이상'", ages[4]], ["'기타'", ages[5]]]

    age_cnt = 0
    for item in ages:
        age_cnt += item
    if age_cnt == 0:
        dictionary[data_type + '_age'] = 0
    else:
        dictionary[data_type + '_age'] = 1

    dictionary[data_type + '_gender_arr'] = gender_arr
    dictionary[data_type + '_age_arr'] = age_arr


def get_column_chart(visit, down_coupon, use_coupon, dictionary):
    set_column_chart(down_coupon, dictionary, 'coupon_down')
    set_column_chart(use_coupon, dictionary, 'coupon_use')
    set_column_chart(visit, dictionary, 'visit')


def set_column_chart(data, dictionary, data_type):
    prefix_gender_arr = ["'month'", u"'합계'", u"'남성'", u"'여성'", u"'기타'"]
    prefix_age_arr = ["'month'", u"'합계'", u"'10대이하'", u"'20대'", u"'30대'", u"'40대'", u"'50대이상'", u"'기타'"]
    age_arr = []
    gender_arr = []

    for i in range(1, 13):
        prefix = "%d" % i
        if data_type == 'visit':
            mon_data = data.filter(visit_date__month=i)
            data_count = data.filter(visit_date__month=i).count()
            woman = data.filter(visit_date__month=i, member__gender=True).count()
            man = data.filter(visit_date__month=i, member__gender=False).count()
        else:
            mon_data = data.filter(regdate__month=i)
            data_count = data.filter(regdate__month=i).count()
            woman = data.filter(regdate__month=i, member__gender=True).count()
            man = data.filter(regdate__month=i, member__gender=False).count()
        etc = data_count - woman - man

        gender_arr.append([prefix, data_count, man, woman, etc])

        today = datetime.datetime.today()
        ages = [(prefix), data_count, 0, 0, 0, 0, 0, 0]

        for tmp in mon_data:
            m = Member.objects.filter(id=tmp.member.id)
            if len(m) == 1:
                if tmp.member.birthday:
                    age_tmp = int(math.floor((today.year - tmp.member.birthday.year + 1) / 10))
                    if age_tmp > 5:
                        ages[6] += 1
                    elif age_tmp == 0:
                        ages[2] += 1
                    else:
                        ages[age_tmp + 1] += 1
                else:
                    # 회원의 나이를 알 수 없을때
                    ages[7] += 1

        age_arr.append(ages)

    dictionary[data_type + '_gender_arr'] = gender_arr
    dictionary[data_type + '_age_arr'] = age_arr
    dictionary['prefix_gender_arr'] = prefix_gender_arr
    dictionary['prefix_age_arr'] = prefix_age_arr


def get_store(user, s_id):
    if user.is_staff is True:
        st = Store.objects.filter(id=s_id, visible_flag=True)
    else:
        st = Store.objects.filter(user=user, id=s_id, visible_flag=True)

    if len(st) == 0:
        return None
    else:
        return st[0]


def get_notice(user, n_id):
    notice = Notice.objects.filter(id=n_id)

    if len(notice) == 0:
        return None
    else:
        return notice[0]


def get_push(user, p_id):
    push = Push.objects.filter(id=p_id)

    if len(push) == 0:
        return None
    else:
        return push[0]


def get_review(user, r_id):
    review = StoreReview.objects.filter(id=r_id)

    if len(review) == 0:
        return None
    else:
        if user != review[0].store.user:
            return None
        else:
            return review[0]


def get_page_list(request, page_number=1, page_size=0, total_count=0):
    page_number = int(page_number)
    if page_size > 0:
        page_size = page_size
    else:
        page_size = 25

    start_offset = (page_number - 1) * page_size
    end_offset = start_offset + page_size

    start_page = 1
    end_page = int(total_count / page_size)

    if float(total_count) / page_size - total_count / page_size:
                end_page = end_page + 1

    paging_list = []
    for i in range(page_number - 5, page_number + 5):
        if i > 0 and i <= end_page:
            paging_list.append(i)

    dic = {
        "start_page": start_page,
        "end_page": end_page,
        "paging_list": paging_list,
        "current_page": page_number,
        "start_offset": start_offset,
        "end_offset": end_offset,
        }

    return dic


def delete(request, obj=None, id=0):
    if request.user.is_anonymous() is True:
        return HttpResponseRedirect('/')

    result = '/'
    if obj == 'StoreReview':
        if request.user.is_staff is True:
            return HttpResponse(u'<script>alert("가맹점으로 로그인 후 이용 바랍니다.");location.href="/";</script>')
        sr = get_review(request.user, id)
        if sr is None:
            return HttpResponseRedirect("/review/list")
        sr.delete()
        result = '/review/list'
    elif obj == 'store':
        s = get_store(request.user, id)
        if s is None:
            return HttpResponseRedirect("/")
        s.visible_flag = False
        s.save()
        result = '/logout/'
    elif obj == 'board':
        board = get_board(request.user, id)
        if board is None:
            return HttpResponseRedirect("/board/list")
        if board.reply_flag == True:
            BoardReply.objects.get(board=board).delete()
        board.delete()
        result = '/board/list'
    elif obj == 'notice':
        if request.user.is_staff is False:
            return HttpResponseRedirect("/")
        notice = get_notice(request.user, id)
        if notice is None:
            return HttpResponseRedirect("/notice/list")
        notice.delete()
        result = '/notice/list'
    elif obj == 'push':
        if request.user.is_staff is False:
            return HttpResponseRedirect("/")
        push = get_push(request.user, id)
        if push is None:
            return HttpResponseRedirect("/push/list")
        push_send(push.id, 1)
        push.delete()
        result = '/push/list'
    elif obj == 'point':
        if request.user.is_staff is False:
            return HttpResponseRedirect("/")
        bill = Bill.objects.filter(id=id)
        if len(bill) == 1:
            bill = bill[0]
            bill.visible_flag = False
            bill.save()

        result = '/point/register'

    return HttpResponseRedirect(result)


def get_url(request, dictionary):
    dictionary['url'] = request.path[1:-1]


def get_times(dictionary):
    years = []
    funing_years = []
    birth_years = []
    months = []
    days = []
    hours = []
    minutes = []
    weeks = [u'월', u'화', u'수', u'목', u'금', u'토', u'일', u'공휴일']
    today = datetime.datetime.today()

    for n in range(2012, 2021):
        years.append((u'%4d' % n))

    for n in range(1950, today.year + 1):
        birth_years.append((u'%4d' % n))

    for n in range(1, 13):
        months.append((u'%02d' % n))

    for n in range(1, 32):
        days.append((u'%02d' % n))

    for n in range(0, 24):
        hours.append((u'%02d' % n))

    for n in range(0, 60):
        minutes.append((u'%02d' % n))

    for n in range(2012, today.year + 1):
        funing_years.append((u'%4d' % n))

    dictionary['years'] = years
    dictionary['birth_years'] = birth_years
    dictionary['months'] = months
    dictionary['days'] = days
    dictionary['hours'] = hours
    dictionary['minutes'] = minutes
    dictionary['today'] = today
    dictionary['week_list'] = weeks
    dictionary['funing_years'] = funing_years


def load_map(request):
    variables = RequestContext(request)
    return render_to_response('map.html', variables)


def info_popup(request):
    variables = RequestContext(request)
    return render_to_response('info_popup.html', variables)


def start_popup(request):
    variables = RequestContext(request)
    return render_to_response('start_popup.html', variables)


def assent_popup(request):
    variables = RequestContext(request)
    return render_to_response('assent_popup.html', variables)
