#-*- coding:UTF-8 -*-
from ticket_backend.models import Catagory, User, Author, Media, Activity, Ticketrequest
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from django.utils.timezone import utc
from excel_response import ExcelResponse
import datetime
#import xlwt
import random
import json

# Create your views here.

def admin_auth(request):
    if request.user.is_authenticated():
        return activity_list(request)
    else:
        #用户未登录，转入登录画面
        return render(request, "admin_auth.html", {"request":request})

def login_view(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        #验证成功，转入活动列表
        login(request, user)    
        print request.user    
        return activity_list(request)
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def logout_view(request):
    logout(request)
    #注销，转入登录画面
    return admin_auth(request)

def activity_list(request):
    if request.user.is_authenticated():
        #验证成功，转入活动列表
        activities = Activity.objects.all()
        catagories = Catagory.objects.all()
        return render(request, "activity_list.html", {"activities": activities, "catagories": catagories, "request":request})
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def activity_list_json(request):
    all_activities = Activity.objects.all()
    activities_valid = []
    for single_activity in all_activities:
        if (single_activity.activity_time > datetime.datetime.utcnow().replace(tzinfo=utc)):
            if (single_activity.posters != None):
                temp = {'id':single_activity.id,
                        'caption':single_activity.caption,
                        'poster':'/media/'+single_activity.posters.image.url,
                        'number':single_activity.ticket_number,
                        'activity_time':str(single_activity.activity_time),
                        'deadline':str(single_activity.request_deadline)}
            else:
                temp = {'id':single_activity.id,
                        'caption':single_activity.caption,
                        'poster':'/media/noPic.jpg',
                        'number':single_activity.ticket_number,
                        'activity_time':str(single_activity.activity_time),
                        'deadline':str(single_activity.request_deadline)}
            activities_valid.append(temp)
    return HttpResponse(json.dumps(activities_valid, ensure_ascii=False))

def user_info_json(request, card_id=''):
    try:
        user_requested = User.objects.get(card_id=card_id)
    except Activity.DoesNotExist:
        raise Http404
    all_requests = Ticketrequest.objects.all();
    related_requests = []
    for single_request in all_requests:
        if single_request.person == user_requested:
            temp = {'ticket_request':single_request.target.caption,
                    'request_time':str(single_request.request_time),
                    'result':single_request.accepted,}
            related_requests.append(temp)
    user_info = {'card_id':card_id,
                 'name':user_requested.name,
                 'history':related_requests}
    return HttpResponse(json.dumps(user_info, ensure_ascii=False))

def sign_up(request, activity_id='', card_id=''):
    try:
        activity_requested = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        raise Http404
    try:
        user_requested = User.objects.get(card_id=card_id)
    except User.DoesNotExist:
        raise Http404
    #检查是否已经超过了报名截止时间
    if (activity_requested.request_deadline > datetime.datetime.utcnow().replace(tzinfo=utc) and activity_requested.request_begin_time < datetime.datetime.utcnow().replace(tzinfo=utc)):
        new_request = Ticketrequest(target = activity_requested,
                                    person=user_requested,
                                    accepted = False)
        new_request.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('not in legal time period')

def activity_show(request, id=''):
    if request.user.is_authenticated():
        try:
            activity = Activity.objects.get(id=id)
        except Activity.DoesNotExist:
            raise Http404
        catagories = Catagory.objects.all()
        return render(request, "activity_show.html", {"activity": activity, "catagories": catagories, "request":request})
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def activity_catagory(request, catagory_name=''):
    if request.user.is_authenticated():
        all_activities = Activity.objects.all()
        catagories = Catagory.objects.all()
        activities_f = []
        for single_activity in all_activities:
            try:
                all_catagories = single_activity.catagories.all()
                filter_catagory = all_catagories.get(catagory_name = catagory_name)
                activities_f.append(single_activity)
            except Catagory.DoesNotExist:
                continue
        return render(request, "activity_catagory.html", {"filter_catagory": catagory_name, "activities": activities_f, "catagories": catagories, "request":request})
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def activity_gen_result(request, id=''):
    if request.user.is_authenticated():
        #验证成功，生成抽取结果
        try:
            target_activity = Activity.objects.get(id=id)
        except Activity.DoesNotExist:
            raise Http404
        #首先判断是否已经抽过
        if target_activity.tickets_dispatched == False:
            #然后判断是否已经超过申请截止日期
            if target_activity.request_deadline < datetime.datetime.utcnow().replace(tzinfo=utc):
                all_requests = []
                for person in target_activity.ticket_requests.all():
                    single_request = Ticketrequest.objects.get(target=target_activity, person=person)
                    all_requests.append(single_request)
                #现在已经在all_requests中存放了所有的request，如果申请数比总发放票数少，则所有申请都成功，反之则pop出发票数量个申请，设定为成功
                if (len(all_requests) <= target_activity.ticket_number):
                    for single_request in all_requests:
                        single_request.accepted = True
                        single_request.save()
                else:
                    for n in range(target_activity.ticket_number()):
                        lucky_request = all_requests.pop(random.randrange(len(all_requests)))
                        lucky_request.accepted = True
                        lucky_request.save()
                #设置tickets_dispatched为True
                target_activity.tickets_dispatched = True
                target_activity.save()
                return activity_show_result(request, id)
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def activity_show_result(request, id=''):
    if request.user.is_authenticated():
        #验证成功，转入显示页面
        try:
            target_activity = Activity.objects.get(id=id)
        except Activity.DoesNotExist:
            raise Http404
        success_requests = []
        for person in target_activity.ticket_requests.all():
            single_request = Ticketrequest.objects.get(target=target_activity, person=person)
            if single_request.accepted == True:
                success_requests.append(single_request)
        return render(request, "result_show.html", {"activity": target_activity, "result_requests":success_requests, "request":request})
    else:
        #验证失败，转入登录画面
        return admin_auth(request)

def activity_result_excel(request, id=''):
    if request.user.is_authenticated():
        #验证成功，转入显示result_excel页面
        try:
            target_activity = Activity.objects.get(id=id)
        except Activity.DoesNotExist:
            raise Http404
        success_requests = []
        data = [[target_activity.caption]]
        data.append([u'总可发放票数', str(target_activity.ticket_number)])
        for person in target_activity.ticket_requests.all():
            single_request = Ticketrequest.objects.get(target=target_activity, person=person)
            if single_request.accepted == True:
                success_requests.append(single_request)
        data.append([u'实际发放票数', str(len(success_requests))])
        for single_request in success_requests:
            data.append([single_request.person.card_id, single_request.person.name])
        return ExcelResponse(data, 'result')
    else:
        #验证失败，转入登录画面
        return admin_auth(request)


def add(request):
    if request.method == 'POST':
        temp = Activity(
            caption=request.POST['actCaption'],
            actType=request.POST['actType'],
            Author=request.POST['Author'],
            # actAuthor=request.POST['actAuthor'],
            activity_time=request.POST['actTime'],
            activity_place=request.POST['actPlace'],
            destruction=request.POST['actDestruction'],
            ticket_number=request.POST['ticketNum'],
            # request_begintime=request.POST['ticketBegin'],
            # request_deadline=request.POST['ticketEnd'],
        )
        temp.save()
    else :
        message = 'You submitted an empty form.'
        return HttpResponse(message)