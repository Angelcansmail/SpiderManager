#!/usr/bin/python
#coding:utf-8
from ThreadTool import ThreadTool
import datetime
import time
import connectpool
from TaskTool import TaskTool
import SQLTool
from lxml import etree as etree
from lxml.html import fromstring
import lxml.html
import lxml.html.soupparser
try:
	from bs4 import UnicodeDammit             # BeautifulSoup 4

	def decode_html(html_string):
		converted = UnicodeDammit(html_string)
		if not converted.unicode_markup:
			raise UnicodeDecodeError("Failed to detect encoding, tried [%s]",', '.join(converted.tried_encodings))
# print converted.original_encoding
		return converted.unicode_markup

except ImportError:
	from BeautifulSoup import UnicodeDammit   # BeautifulSoup 3

	def decode_html(html_string):
		converted = UnicodeDammit(html_string, isHTML=True)
		if not converted.unicode:
			raise UnicodeDecodeError("Failed to detect encoding, tried [%s]",', '.join(converted.triedEncodings))
# print converted.originalEncoding
		return converted.unicode
	
	
class dealTask(TaskTool):
	##处理任务类，通过将爬虫爬回来的网页信息进行进一步的处理
	def __init__(self,isThread=0):
		TaskTool.__init__(self,isThread)
		self.connectpool=connectpool.ConnectPool()

	def task(self,req,threadname):
		print threadname+' 执行dealTask任务中'+str(datetime.datetime.now())
		ans = self.makesqlit(req)

		print threadname+' dealTask任务结束'+str(datetime.datetime.now())
		return ans

	def makesqlit(self,content):
		try:
			dom = lxml.html.fromstring(decode_html(content))
			ignore = lxml.html.tostring(dom, encoding='unicode')
		except UnicodeDecodeError:
			dom = lxml.html.soupparser.fromstring(content)
		page = etree.HTML(content)
		print page
	
		'''
		for index in range(len(dom)):
			for item in dom[index]:
				print ("index[%d]\ttag:%s\tparent_tag:%s"%(index, item.tag, item.getparent().tag))
		'''
		# hrefs = dom.xpath(u"//@href")
		hrefs = dom.xpath(u"//a")#xpath的路径可以采用xpath checker火狐插件自动生成
		result=[]
		print "hrefs length:", len(hrefs)
		for href in hrefs:
			print href.attrib
			if 'href' in href.attrib.keys():
				# print ("href:%s\ttext:%s "%(href.attrib['href'], href.text))
				result.append(href.attrib['href'])
		return result

if __name__ == "__main__":
	"""
	DealSQL=SQLTool.DBmanager()
	DealSQL.connectdb()
	(result,title,count,col)=DealSQL.searchtableinfo_byparams(['webdata'],['address','content','meettime'])
	DealSQL.closedb()
	#TODO 添加元组进去
	#ｕｒｌ也要存进去
	f = dealTask()
	f.set_deal_num(10)


	for data in result:
		f.add_work([(data[0],data[1])])
#		print data[1]

	f.start_task()
	while f.has_work_left():
		v,ans=f.get_finish_work()
		print ans
	while True:
		pass

	"""

	try:
		file_object = open('20155273')
		content = file_object.read( )
		file_object.close( )
	except Exception,e:
		print e
	TOOL = dealTask()
	TOOL.set_deal_num(1)
	TOOL.add_work([content])

# 	TOOL.start_task()
	while TOOL.has_work_left():
		res, ans = TOOL.get_finish_work()
		print ("ans_len%d\n----------------ans----------------\n%s"%(len(ans), ans))
# res is content, ans save the content's url
#		print ("----------------res----------------\n%s\n----------------ans----------------\n%s"%(res, ans))
	#array=TOOL.makesqlit(content)
	#print array


