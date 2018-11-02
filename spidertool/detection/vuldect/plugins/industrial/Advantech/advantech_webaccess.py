#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..t import T
import urllib2
import requests

import bs4
import lxml.html
import re
import sys
import ssl
from urllib2 import urlopen
import socket
import traceback
from termcolor import cprint

reload(sys)
sys.setdefaultencoding('utf8')

socket.setdefaulttimeout(10)

class P(T):
    def __init__(self):
	T.__init__(self)

    def verify(self, head='', context='', ip='', port='80', productname={}, keywords='', hackresults=''):
	result = {}
	result['result'] = False

	html_content = context
#	print "Advantech::verify() context:", html_content
	try:
	    if port == '443':
		target_url = 'https://' + ip + ':' + port
	    else:
		target_url = 'http://' + ip + ':' + port 

	    '''
    	    context = ssl._create_unverified_context()
	    response = urllib2.urlopen(url=target_url, context=context)

            html_content = response.read()
	    '''
	except Exception, e:
            print target_url, "connect time out\n", traceback.print_exc()
	    return result
	if 'Advantech' in html_content:
	    cprint(target_url + '可能存在漏洞(版本有待检测)', 'orange')
	    info = target_url + " Advantech Webaccess"
	    result['result']=True
	    result['VerifyInfo'] = {}
	    result['VerifyInfo']['type']='Advantech Webaccess Vul'
	    result['VerifyInfo']['URL'] = target_url
	    result['VerifyInfo']['payload'] = 'Advantech Webaccess Vul'
	    result['VerifyInfo']['result'] = info
	    result['VerifyInfo']['level'] = 'hole'
	    return result
	return result

if __name__ == '__main__':
    print P().verify(ip='180.76.176.35')


