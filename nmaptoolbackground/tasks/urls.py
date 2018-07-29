#!/usr/bin/python
#coding:utf-8
from django.conf.urls import url

import taskroute as route

urlpatterns = [
    url(r'^$', route.showtask, name='taskshow'),
    url(r'^status/$', route.indexpage, name='status'),
    url(r'^taskquery/$', route.taskquery, name='taskquery'),
    url(r'^addtask/$', route.addtask, name='addtask'),
    url(r'^starttask/$', route.starttask, name='starttask'),
    url(r'^pausetask/$', route.pausetask, name='pausetask'),
    url(r'^destorytask/$', route.destorytask, name='destorytask'),
]
