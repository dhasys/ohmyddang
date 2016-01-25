# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cms.models import *
from django.contrib.auth.models import User
from wand.image import Image
from urllib2 import urlopen
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from gcm import GCM
from django.db.models import Sum
import os
import datetime


_COUPON_POINT = 50


def store_login_required(functor):
    def decorated(request, *args, **kargs):
        if request.user.is_staff is False:
            return functor(request, *args, **kargs)
        else:
            return HttpResponse(u'<script>alert("가맹점으로 로그인 후 이용 바랍니다.");location.href="/";</script>')

    return decorated


def validate_user(user, store_id):
    if len(Store.objects.filter(id=store_id)) == 0:
        return False
    else:
        if user.is_staff is False and user != Store.objects.get(id=store_id).user:
            return False


def api_decorator(functor):
    def decorated(request, *args, **kargs):
        if request.get_full_path().startswith(u'/api/'):
            return functor(request, *args, **kargs)
        else:
            return login_required(functor)(request, *args, **kargs)

    return decorated


def member_login_duplicate_check(data):
    idCount = Member.objects.filter(
        udid=data['member_id']
    ).count()
    nickCount = 0
    if len(data['member_nickname']) > 0:
        nickCount = Member.objects.filter(
            nickname=data['member_nickname']
        ).count()

    default = ''
    returnVal = ''
    if idCount > 0:
        val = False
        default = HttpResponse("id")
    elif nickCount > 0:
        val = False
        default = HttpResponse("nick")
    else:
        val = True
        default = HttpResponse("ok")

    if 'isResponse' in data:
        if data['isResponse'] == 'true':
            returnVal = default
    else:
        returnVal = val

    return returnVal


def member_login_check(udid):
    members = Member.objects.filter(udid=udid)
    if len(members) > 0:
        # 모델의 last_login_time 업데이트되는 부분이 자동으로 처리되면 빠져도 됨.
        member = Member.objects.get(udid=udid)
        member.save()

        if member.nickname is not "":
            data = {'result': True,
                    'member_id': member.id,
                    'member_nickname': member.nickname,
                    'birthday': None,
                    'gender': member.gender,
                    'push': member.push_acceptable
                    }
        else:
            data = {'result': True,
                    'member_id': member.id,
                    'member_nickname': member.nickname,
                    'birthday': member.birthday.strftime("%Y-%m-%d"),
                    'gender': member.gender,
                    'push': member.push_acceptable
                    }

        return data
    else:
        return {'result': False}


def get_store_list(geo):
    store_list = Store.objects.all()

    st_ist = []
    for st in store_list:
        dic = {}
        dic['id'] = st.id
        dic['name'] = st.store_name
        dic['lat'] = st.latitude
        dic['lng'] = st.longitude
        dic['coupon'] = get_store_coupon(st)

        if st.prime_image != None:
            dic['cPrime'] = st.prime_image.compress_image.url
        st_ist.append(dic)

    return st_ist


def get_store_coupon(st):
    coupon = Coupon.objects.filter(store=st)
    count = 0
    if len(coupon) > 0:
        for cp in coupon:
            status = get_coupon_status(cp)
            if status == u'발행중':
                count += 1
    return count


# 상점정보 저장
def set_store(dataStore):
    users = User.objects.filter(username=dataStore['store_id'])
    if len(users) > 0:
        user = User.objects.get(username=dataStore['store_id'])
        store = Store.objects.get(user_id=user.id)
        user.delete()
        store.delete()
        return dataStore['store_name'] + ' delete'
    else:
        user = User()
        user.username = dataStore['store_id']
        user.set_password(dataStore['password'])
        user.email = dataStore['email']
        user.is_staff = False
        user.save()

        store = Store()
        store.user = user
        store.store_name = dataStore['store_name']
        store.president_name = dataStore['president_name']
        store.business_number = dataStore['business_number']
        store.category = dataStore['category']
        store.manager_name = dataStore['manager_name']
        store.manager_phone = dataStore['manager_phone']
        store.address = dataStore['address']
        store.description = dataStore['description']
        store.longitude = dataStore['longitude']
        store.latitude = dataStore['latitude']
        store.dayoff = dataStore['dayoff']
        store.open_time = dataStore['open_time']
        store.close_time = dataStore['close_time']
        store.search = dataStore['store_name'].strip().replace(" ", "") + '|' + dataStore['president_name'].strip().replace(" ", "")

        pic = picture_save_api(request_file=dataStore['prime_image'], original_file_size=(184, 184), original_file_type='gif', compress_file_type='gif', compress_file_size=(65, 65))
        store.prime_image = pic
        store.save()

        for file_str in dataStore['pictures_images']:
                pic = picture_save_api(request_file=file_str, compress_file_size=(140, 140))
                store.pictures.add(pic)
                store.save()

        return dataStore['store_name'] + ' save'


def picture_save_api(request_file, original_file_size=(0, 0), original_file_type='jpeg', compress_file_size=(0, 0), compress_file_type='jpeg'):
    pic = Picture()
    pic.save()

    original_image = Image(file=urlopen(request_file))
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


def exist_dir_check(path, dir_n):
    d = path + '/%d' % dir_n
    if os.path.exists(d) == False:
        os.makedirs(d)
    return d + '/'


def get_image_path(id, type):
    p = Picture.objects.get(id=id)
    d = p.id / 1000
    path = '/static/' + type + '/' + str(d) + '/' + p.image_name
    return path


def get_store_detail_info(json_data):
    # 사용자가 요청한 상점의 상세정보를 알려줌.
    store_id = json_data['store_id']
    dic = {}
    # 쿠폰 포인트의 디폴트값이 정해져 있어야함.
    if json_data['type'] == 'merchant':
        store = Store.objects.filter(id=store_id)
        if len(store) > 0:
            store = store[0]
            dic['name'] = store.store_name
            #dic['work_open'] = store.open_time[:2] + ":" + store.open_time[2:]
            #dic['work_close'] = store.close_time[:2] + ":" + store.close_time[2:]
    elif json_data['type'] == 'store':
        #member_id = json_data['member_id']
        store = Store.objects.filter(id=store_id)
        if len(store) > 0:
            store = store[0]
            req = {}
            dic['id'] = store_id
            dic['name'] = store.store_name
            dic['tel'] = store.manager_phone
            #dic['work'] = store.open_time[:2] + ":" + store.open_time[2:] + "~" + store.close_time[:2] + ":" + store.close_time[2:]

            # 해당 사용자의 udid 값을 체크한 후에 사용자가 좋아요를 눌렀는지 확인.
            #member = Store.objects.filter(id=member_id)[0]
            #likes = Like.objects.filter(member=member, store=store)
            #if len(likes) > 0:
            #    dic['islike'] = True
            #else:
            #    dic['islike'] = False
            
            dic['cLike'] = Like.objects.filter(store=store).count()

            # 상점의 방문자 카운팅 가져오기.
            #req['member'] = member
            req['store'] = store
            #set_store_visit(req)
            visit_count = Visit.objects.filter(store=store).count()
            dic['cVis'] = visit_count

            coupon_count = Coupon.objects.filter(store=store).count()

            dic['coupon'] = coupon_count
            dic['description'] = store.description
            #dic['lat'] = store.latitude
            #dic['lng'] = store.longitude

            # if store.prime_image != None:
            if store.prime_image != None:
                dic['oPrime'] = store.prime_image.original_image.url

            store_original_pictures = []
            store_compress_pictures = []
            pictures = store.pictures.all()
            for i in pictures:
                store_compress_pictures.append(i.compress_image.url)
                store_original_pictures.append(i.original_image.url)
            dic['oPic'] = store_original_pictures
            dic['cPic'] = store_compress_pictures
            
            results = get_coupon_extra_point(store_id)
            print results
            dic['subscription'] = results['subscription']
            dic['extrapoint'] = results['extrapoint']
            

    return dic


# 상점에 대한 좋아요 카운팅.
def set_store_like(req):
    store = Store.objects.filter(id=req['sid'])
    dic = {}
    if len(store) > 0:
        store = Store.objects.get(id=req['sid'])

        member = Member.objects.get(udid=req['id'])
        likes = Like.objects.filter(member=member, store=store)
        if len(likes) > 0:
            like = Like.objects.get(member=member, store=store)
            like.delete()
            dic['result'] = 'like'
        else:
            like = Like()
            like.store = store
            like.member = member
            like.save()
            dic['result'] = 'unlike'
    return dic


# 오늘 이 사용자가 해당 상점에 방문했는지 체크.
def set_store_visit(req):
    today = datetime.date.today()
    tommorw = today + datetime.timedelta(days=1)
    visits = Visit.objects.filter(member=req['member'], store=req['store']
        ).filter(visit_date__range=(today, tommorw)).count()

    if visits is 0:
        # 현재 날짜와 이전의 방문 날짜를 비교하여서 뭔가를 업데이트 시킴.
        visit = Visit()
        visit.member = req['member']
        visit.store = req['store']
        visit.save()


def check_store_login(req):
    user = authenticate(username=req['username'], password=req['password'])
    dic = {}
    if user is not None:
        if user.is_active:
            if user.is_staff:
                dic['result'] = False
            else:
                store = Store.objects.get(user=user)
                if store.activate_flag is True:
                    dic['result'] = True
                    dic['id'] = store.id
                    dic['store_type'] = store.store_type
                    dic['msg'] = '성공'
                else:
                    dic['result'] = False
                    dic['msg'] = '가입승인이 완료되지 않았습니다.'
        else:
            dic['result'] = False
            dic['msg'] = '가입승인이 완료되지 않았습니다.'
    else:
        dic['result'] = False
        dic['msg'] = '아이디 혹은 비밀번호가 틀립니다.'
    return dic


def push_send(push_id, push_type):
    # push_type = 0,1
    # 0 : 즉시발송
    # 1 : 푸쉬삭제
    API_KEY = 'AIzaSyByl17d2XCjWqZy4Wa7RaWmlsbkB1bGfHs'
    reg_ids = []

    # 푸시 보낼 사용자 선택.
    members = Member.objects.filter(push_acceptable=True)
    response = 'member is 0'
    if len(members) > 0:
        for member in members:
            reg_ids.append(member.push_id)

        # 푸시에 사용될 메시지 가져오기.
        push = Push.objects.filter(id=push_id)
        if len(push) > 0:
            push = Push.objects.get(id=push_id)

        # 푸시 메시지 생성.
        gcm = GCM(API_KEY)
        date = str(push.activated_date_time).replace(" ", "-").replace(":", "-")
        date = date[:date.find('.')]
        data = {'subject': 'Funing', 'contents': push.contents, 'date': date, 'id': push_id, 'type': int(push_type)}

        # 푸시 보내기.
        response = gcm.json_request(registration_ids=reg_ids, data=data)

        # 푸시 에러 핸들링.
        if 'errors' in response:
            for error, reg_ids in response['errors'].items():
                # Check for errors and act accordingly
                if error is 'NotRegistered':
                    # Remove reg_ids from database
                    for reg_id in reg_ids:
                        # print reg_id
                        Member.objects.get(push_id=reg_id).delete()
        if 'canonical' in response:
            for canonical_id, reg_id in response['canonical'].items():
                # print 'canonical_id : %s' % canonical_id
                # print 'reg_id : %s' % reg_id
                # Repace reg_id with canonical_id in your database
                member = Member.objects.get(push_id=canonical_id)
                member.push_id = reg_id
                member.save()

    return response


def check_coupon_time(coupon):
    today = datetime.datetime.today()
    act_time = '%02d%02d' % (coupon.activated_date_time.hour, coupon.activated_date_time.minute)
    exp_time = '%02d%02d' % (coupon.expired_date_time.hour, coupon.expired_date_time.minute)
    time = '%02d%02d' % (today.hour, today.minute)
    if act_time < time and time < exp_time:
        return True
    else:
        return False


def get_order_status(cp):
    if  cp.status == 0:
        status = u"주문접수"
    elif cp.status == 1:
        status = u"배송준비"
    elif cp.status == 2:
        status = u"배송완료"
    elif cp.status == 3:
        status = u"구매확정"    
        
    return status


def get_coupon_status(cp):
    if  cp.publish_flag == True:
            status = u"발행중"
    elif cp.publish_flag == False:
        status = u"발행중지"

    return status





# extrapoint, 정액제 여부
def get_coupon_extra_point(store_id):
    store = Store.objects.filter(id=store_id)
    result = {}

    if len(store) != 1:
        result['result'] = False
    else:
        store = store[0]
        if store.activate_flag == True:
            result['result'] = True
            result['available_cnt'] = 0
            today = datetime.datetime.today()
            subscription_mybill = MyBill.objects.filter(store=store, useable=True, activated_date__lte=today, expired_date__gte=today)
            if len(subscription_mybill) > 0:
                result['subscription'] = True
                return result

            mybill = MyBill.objects.filter(store=store, useable=True, activated_date=None, expired_date=None)
            if len(mybill) > 0:
                sum_point = mybill.aggregate(Sum('point'))['point__sum']
                use_point = MyCoupon.objects.filter(coupon__store=store, subscription_flag=False).count() * _COUPON_POINT
                extra_point = sum_point - use_point
                # 발행중인 등록된 쿠폰의 개수들의 합.
                coupons = Coupon.objects.filter(store=store, visible_flag=True )
                total_cnt = Coupon.objects.filter(store=store, visible_flag=True).aggregate(Sum('count'))['count__sum']
                # my_coupon_cnt = MyCoupon.objects.filter(coupon__store=store, subscription_flag=False).count()
                # 발행중인 쿠폰들중에 다운받은 쿠폰의 개수 차감하기위하여.
                publish_down_cnt = 0
                for cp in coupons:
                    publish_down_cnt += MyCoupon.objects.filter(coupon=cp).count()

                result['subscription'] = False
                result['extrapoint'] = int(extra_point)

                if total_cnt == None:
                    total_cnt = 0

                result['total_cnt'] = int(total_cnt)
                # result['available_cnt'] = int((extra_point / _COUPON_POINT) - total_cnt) + my_coupon_cnt
                result['available_cnt'] = int((extra_point / _COUPON_POINT) - total_cnt) + publish_down_cnt
                # print 'sum::%d pt ||  use:%d pt || extra_pt:: %d pt || 발행중쿠폰개수 :: %d ||  발행중인쿠폰중 다운:: %d  ||' % (sum_point, use_point, extra_point, total_cnt, publish_down_cnt)
        else:
            result['result'] = False

    return result