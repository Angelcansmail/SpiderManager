#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: gzh
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 937f5a138eb9c25ba5be79214f48bd31@qq.com
@software: PyCharm
@file: nginx_http_mp4_module.py
@time: 2018/11/30 14:48
@desc:
'''

from ..miniCurl import Curl
from ..t import T
import urlparse
import re

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        result = {}
        result['result']=False

        return result