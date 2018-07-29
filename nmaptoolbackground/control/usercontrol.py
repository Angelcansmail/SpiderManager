#!/usr/bin/python
# -*- coding: utf-8 -*-

from spidertool import SQLTool, config

localconfig=config.Config()

def validuser(username,password):
    validresult=False
    DBhelp=SQLTool.DBmanager()
    DBhelp.connectdb()
	# result = sql's result; ({'username': 'admin', 'role': '3', 'userpower': '3'},) 
	# content = sql's some content, don't know what it is to use
	# conunt = result's count; col = 第二个参数的个数
    result, content, count, col=DBhelp.searchtableinfo_byparams([localconfig.usertable], ['username','role','userpower'], ['username','password'], [SQLTool.formatstring(username),SQLTool.formatstring(password)], order='username desc')
    DBhelp.closedb()
    role = ''
    userpower = ''
    if col > 0:
        validresult = True
        role = result[0]['role']
        userpower = result[0]['userpower']
#         role=result[0][1]
#         userpower=result[0][2]
    return validresult, username, role, userpower

