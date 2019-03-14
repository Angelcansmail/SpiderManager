#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/25 13:45
@Author  : gzh
@contact : k39aE465wlulvnkhT0i9MQ==@qq.com
@Site    : 
@File    : __init__.py.py
@Desc    : 
@Software: PyCharm
"""


KEYWORDS = ['kibana', ]

def rules(head='', context='', ip='', port='', productname={}, keywords='', hackresults=''):
    if port in '5601':
        return True
    else:
        return False