#!/usr/bin

import re
cmd = "zmap -w spidertool/iparea.json -B 1M -p 3306 -N 10 -q -O json"

from spidertool import commandtool
returnmsg = commandtool.command(cmd=cmd)    
p = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
ip_list = p.findall(returnmsg)
print len(ip_list)

for ip in ip_list:
    print ip
