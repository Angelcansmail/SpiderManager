#! /usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from django.views.generic import RedirectView

from . import nmaproute as route

urlpatterns  =  [
    # nmaptool/sigin
    url(r'^$', route.indexpage, name = 'login'),
    url(r'^sigin$', route.sigin, name = 'sigin'),
    url(r'^login$', route.login, name = 'login'),
    url(r'^logout$', route.logout, name = 'logout'),
    url(r'^userinfo$', route.userinfo, name = 'userinfo'),

    url(r'^mainpage$', route.indexpage, name = 'index'),
	url(r'^groupitem$', route.groupitem, name = "groupitem"),
	url(r'^taskdetail$',route.taskdetail,name = 'taskdetail'),
	url(r'^taskdetail/eachtask$', route.ipmain, name = 'ipmain'),

    url(r'^jobshow$',route.jobshow, name = 'jobshow'),
    url(r'^addjob$',route.addjob, name = 'addjob'),
    url(r'^startjob$',route.startjob, name = 'startjob'),
    url(r'^pausejob$',route.pausejob,name = 'pausejob'),
    url(r'^destroyjob$',route.destroyjob,name = 'destroyjob'),

    url(r'^chartshow$',route.chartshow,name='chartshow'),      
    url(r'^chartdata$',route.chartdata,name='chartdata'),

    url(r'^getwork$',route.getwork,name='getwork'),      
    url(r'^uploadipinfo$',route.upload_ip_info,name='uploadipinfo'),
    url(r'^uploadportinfo$',route.upload_port_info,name='uploadportinfo'),

    url(r'^systeminfo$', route.systeminfo, name='systeminfo'),

    url(r'^tasks/', include('nmaptoolbackground.tasks.urls', namespace = 'tasks')),
]
