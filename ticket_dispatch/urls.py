# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from ticket_backend.views import login_view, logout_view, activity_list

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ticket_dispatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'activity_list', name='home'),
    #我原本打算替换掉admin里面的ticket_backend/activity/页面，取消下面一行的注释即可替换这个页面
    url(r'^admin/ticket_backend/activity/$', activity_list),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login_view),
    url(r'^accounts/logout/$', logout_view),
    url(r'^activities/', include('ticket_backend.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/teloti/workspace/ticket_dispatch/static'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/teloti/workspace/ticket_dispatch/media'}),
)
