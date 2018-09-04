#!/usr/bin/python
#coding:utf-8
from ThreadTool import ThreadTool
import datetime
import time
import connectpool
import portscantool
import SQLTool,config
from TaskTool import TaskTool

from logger import initLog
portscantskinstance=None

def getObject():
    global portscantskinstance
    if portscantskinstance is None:
        portscantskinstance = PortscanTask(1)
    return portscantskinstance

class PortscanTask(TaskTool):
    def __init__(self, isThread=1, deamon=False):
        TaskTool.__init__(self,isThread,deamon=deamon)
        import Sqldatatask
        self.logger = initLog('logs/portScantask.log', 2, True,'portscantask')
        self.sqlTool = Sqldatatask.getObject()  #init DBmanager
        #init ConnetcPool's parameters, eg: proxy_address, proxy_name...在webconfig.py中设定 
        self.connectpool = connectpool.getObject()
        # timeout:8, config:xxx, socketclient:None
        self.portscan = portscantool.Portscantool()
        self.config = config.Config
        self.set_deal_num(15)

    def task(self,req,threadname):
	# print ("\n======================portscantask::task() req:%s======================\n"%str(req))
        if req[3]!='open':
            return ''
        ip = req[1]
        port = req[2]
        productname = req[4]
        nmapscript = req[5]
        head = None
        page = None
        hackinfo = ''
        keywords = ''
        webkey = ''
        webtitle = ''
        self.logger.info('端口%s扫描%s执行任务中%s', port, threadname, str(datetime.datetime.now()))
        # 7001端口是Freak88, Weblogic默认端口
        if (req[0] == 'http' or req[0] == 'https') or (req[0] in ['tcpwrapped','None'] and port in ['80','8080','7001']):
            if ip[0:4]=='http':
                address=ip+':'+port
            else:
                if  port=='443':
                    address='https'+'://'+ip+':'+port
                else:
                    if req[0]=='tcpwrapped' and port in ['80','8080','7001']:
                        address = 'http://' + ip + ':' + port
                    else: # None, 不合法?ftp/smtp...
                        address = req[0]+'://'+ip+':'+port
            # 获取网页反馈的头部和整个网页信息(urllib2, requests)
            head, page = self.connectpool.getConnect(address)
            import webutil
            # 获取网页的关键词和网站标题
            webinfo = webutil.getwebinfo(page)
            webkey = webinfo['keywords']
            webtitle = webinfo['title']
            self.logger.info('webutil.getwebinfo(%s) method_1 \nkeywords:%s\ntitle:%s\n', address, webkey, webtitle)
            
            try:
                # 调用检测功能（http/poc/fuzz，目前只开源了fuzz检测）
                # httpdect(headdect) 可以获得keywords和hackinfo信息, 后续要探究下这部分怎么解析, 所以目前返回的结果为空
                # pocsearch 后续也要加入
                from detection import page_identify
                keywords, hackinfo = page_identify.identify_main(head=head,context=page,ip=ip,port=port,productname=productname,protocol=req[0],nmapscript=nmapscript)
            except:
                pass
        else:
            head, page, keywords, hackinfo = self.portscan.do_scan(head=head,context=page,ip=ip,port=port,name=req[0],productname=productname,nmapscript=nmapscript)
            import webutil
            webinfo = webutil.getwebinfo(page)
            webkey = webinfo['keywords']
            webtitle = webinfo['title']
            self.logger.info('webutil.getwebinfo(%s:%s) method_2 \nkeywords:%s\ntitle:%s\n', ip, str(port), webkey, webtitle)
            pass
#         print page
#         self.sqlTool.connectdb()
        localtime=str(time.strftime("%Y-%m-%d %X", time.localtime()))
        insertdata=[]
        temp = str(page)

        head = SQLTool.escapewordby('{'+head+'}')
        msg = SQLTool.escapewordby('{'+temp+'}')
        hackinfomsg = SQLTool.escapewordby(hackinfo)
        keywords = SQLTool.escapewordby(str(keywords))
        import Sqldata
        insertdata.append((ip,port,localtime,msg,str(head),str(port),hackinfomsg,keywords,webkey,webtitle))
                                         
        extra = ' on duplicate key update  detail=\''+msg+'\' ,head=\''+str(head)+'\', timesearch=\''+localtime+'\',hackinfo=\''+hackinfomsg+'\',keywords=\''+str(keywords)+'\',webkeywords=\''+webkey+'\',webtitle=\''+webtitle+'\''
        sqldatawprk = []
        dic = {"table":self.config.porttable,"select_params":['ip','port','timesearch','detail','head','portnumber','hackinfo','keywords','webkeywords','webtitle'],"insert_values":insertdata,"extra":extra}
        tempwprk = Sqldata.SqlData('inserttableinfo_byparams',dic)
        sqldatawprk.append(tempwprk)
        self.sqlTool.add_work(sqldatawprk)
#         inserttableinfo_byparams(table=self.config.porttable,select_params=['ip','port','timesearch','detail'],insert_values=insertdata,extra=extra)

#         self.sqlTool.closedb()
        self.logger.info('%s 端口扫描　任务结束%s', threadname,str(datetime.datetime.now()))
        return page

if __name__ == "__main__":
    links = [('http','www.ytu.edu.cn','80','open','weblogic','weblogic')]
    f = PortscanTask()
    f.add_work(links)

    while True:
        pass

