#!/usr/bin

import re
cmd = "zmap -w ip_test -B 100M -p 80 -N 10 -q -O json"

from spidertool import commandtool
returnmsg = commandtool.command(cmd=cmd)
print returnmsg

'''
p = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
ip_list = p.findall(returnmsg)
print len(ip_list)

for ip in ip_list:
    print ip
'''


import commands
(status, returnmsg) = commands.getstatusoutput('masscan -p80 139.198.13.163/24')
print status, returnmsg
p = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
ip_list = p.findall(returnmsg)
print len(ip_list)

for ip in ip_list:
    print ip
