#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns(('ticket_backend.views'),
        #活动列表页面
        url(r'^$', 'activity_list', name='activitylist'),
        #详细显示活动信息以及具体操作
        url(r'^(?P<id>\d+)/$', 'activity_show', name='detailactivity'),
        #生成活动结果
        url(r'^(?P<id>\d+)/generate$', 'activity_gen_result', name='genresult'),
        #查看活动结果
        url(r'^(?P<id>\d+)/result$', 'activity_show_result', name='showresult'),
        #请求 Excel 格式结果
        url(r'^(?P<id>\d+)/result_excel$', 'activity_result_excel', name='resultexcel'),
        #分类别筛选活动信息
        url(r'^catagory/(?P<catagory_name>\w+)/$', 'activity_catagory', name='filteractivity'),
        #url(r'^add/$', 'activity_add', name='addactivity'),
        #url(r'^upload/$', 'pic_upload', name='uploadpic'),
        #url(r'^(?P<id>\w+)/update$', 'activity_update', name='updateactivity'),
        #url(r'^(?P<id>\w+)/del/$', 'activity_del', name='delactivity'),
        #url(r'^pictures/$', 'pic_show', name='listmedia'),
        #登录界面，没什么好说的
        url(r'^auth/$', 'admin_auth', name='authpage'),
        #json格式活动列表
        url(r'^activity_list_json$', 'activity_list_json', name='activitylist_json'),
        #json格式个人信息，提交卡号，获取信息和申请记录、结果
        url(r'^user_info_json/(?P<card_id>\d+)$', 'user_info_json', name='user_info_json'),
        #提交报名
        url(r'^(?P<activity_id>\d+)/signup/(?P<card_id>\d+)$', 'sign_up', name='activitysignup'),
        url(r'^add/$','add',name="activityAdd"),
        
)
