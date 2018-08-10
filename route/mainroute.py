#! /usr/bin/python
# -*- coding:utf-8 -*-

import datetime, json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from spidertool import webtool

def indexpage(request):
    now = datetime.datetime.now()
    return render_to_response('index.html', {'current_date': now})

def testdata(request):
    response_data = {}

    ary = []
    item = {}

    item['name']='北京市'
    item['value'] = '119'
    ary.append(item)

    item = {}
    item['name'] = '上海市'
    item['value'] = '120'
    ary.append(item)

    item = {}
    item['name'] = '市'
    item['value'] = '120'
    ary.append(item)

    response_data['citys']=ary

    return HttpResponse(json.dumps(response_data, skipkeys=True, \
            default=webtool.object2dict, encoding='utf8'), \
            content_type="application/json")

