#!/usr/bin/python
#coding:utf-8
from ThreadTool import ThreadTool
import datetime
import time
import SQLTool
from TaskTool import TaskTool

sqltaskdata = None

def getObject():
	global sqltaskdata
	if sqltaskdata is None:
		sqltaskdata = SqlDataTask()
		sqltaskdata.set_deal_num(1)
	return sqltaskdata

class SqlDataTask(TaskTool):
	def __init__(self,isThread=1):
		TaskTool.__init__(self,isThread)
		self.sqlhelp = SQLTool.getObject()  #DBmanager初始化
		self.sqlhelp.connectdb()

	def task(self, req, threadname):
		print threadname + '数据库任务　执行任务中' + str(datetime.datetime.now())
# 		self.sqlhelp.connectdb()
        # 获取存入的数据库操作方法，如getLocationIpInfo中的func:inserttableinfo_params;Dic:对应该操作函数的对应参数字典
		func = req.getFunc()
		Dic = req.getDic()
 		print ("======================func:%s, Dic:%s======================"%(func,Dic))
        # ans 获取存储的功能，getattr(object, name[, default])
		ans = getattr(self.sqlhelp, func, 'default')(**Dic)

		try:
			import sys
			sys.path.append("..")
			from elasticsearchmanage import elastictool

            # 调用elastictool中的func函数，参数通过Dic传过去
			ans = getattr(elastictool, func, 'default')(**Dic)
		except Exception,e:
			print 'error in elasticsearch', e
		del Dic
		
		print threadname+'数据库任务　结束' + str(datetime.datetime.now())

# 		self.sqlhelp.closedb()
		return ans

if __name__ == "__main__":
	links = [ 'http://www.bunz.edu.com','http://www.baidu.com','http://www.hao123.com','http://www.cctv.com','http://www.vip.com']
	
	f = searchTask()
	f.set_deal_num(2)
	f.add_work(links)

	#f.start_task()
	while f.has_work_left():
		v,b = f.get_finish_work()
		
	while True:
		pass


