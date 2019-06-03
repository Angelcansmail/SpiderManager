#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, abspath, join, isdir
from os import listdir
from urlparse import urljoin
from re import compile
import callbackresult
from termcolor import cprint
import traceback

GPocController=None

def getObject():
    global  GPocController
    if  GPocController is None:
        GPocController=PocController()
        GPocController.loadonce()
    return GPocController.getitem()

class PocController(object):
    def __init__(self, logger=None):
        self.modules_list = [
            {'module_name': 'component'},
            {'module_name': 'middileware'},
            {'module_name': 'database'},
            {'module_name': 'basemodel'},
            {'module_name': 'router'},
            {'module_name': 'application'},
            {'module_name': 'industrial'}
        ]
        self.keywords = {}
        self.rules = {}
        self.components = {}
        self.logger = logger
        self.result = None
        self.loadonce()

    def getitem(self):
        return self.keywords,self.rules,self.components

    def loadonce(self):
        self.loader()

    @classmethod
    def __list_plugins(self, module_path):
	# 将当前module下的所有文件名返回
	# ~/component/xampp
	# print "__list_plugins: module_path:%s"%str(module_path)
        return set(map(lambda item: item.endswith(('.py', '.pyc')) and item.replace('.pyc', '').replace('.py', ''), listdir(module_path)))

    # 按照组块下的py文件名称作为映射，并删除t\minicurl\__init__三个公用的非组建
    def __get_component_plugins_list(self,componentname, module_name):
        path = join(abspath(dirname(__file__)), componentname+'/%s' % module_name)
#	self.logger.info("__get_component_plugins_list_path[%s]",str(path))
        plugins_list = self.__list_plugins(path)
#	set(['__init__', 'XAMPP_0513e4ffc8bbb2129805b3ac0e9545ea'])
#	self.logger.info("__get_component[%s:%s]_plugins_list:%s", componentname, module_name, str(plugins_list))
        if False in plugins_list:
            plugins_list.remove(False)
        plugins_list.remove('__init__')
        if 't' in plugins_list:
            plugins_list.remove('t')
        if 'miniCurl' in plugins_list:
            plugins_list.remove('miniCurl')
        return plugins_list

    @classmethod
    def __get_component_detail_list(self,componentname):
        path = join(abspath(dirname(__file__)), componentname)
        modules_list = set(map(lambda item: isdir(join(path, item)) and item, listdir(path)))
#	set([False, 'xampp', 'httpfileserver', 'struts', 'redis', 'openssl', 'joomla', 'cacti', 'fast_cgi', 'zebra', ...])
#	print "__get_component[%s]_detail_list[%s]"%(componentname, str(modules_list))
        if False in modules_list:
            modules_list.remove(False)
        return modules_list

    def __load(self, module_name, plugin_name):
        plugin_name = '%s.%s' % (module_name, plugin_name)
        plugin = __import__(plugin_name,globals=globals(), fromlist=['P'])
#        self.logger.info('Load Plugin: %s.P', plugin_name)
	# 初始化result{type,version}, keywords{}, versions{}
        return plugin.P

    @classmethod
    def __load_keywords(self, componentname, module_name):
        module_name = componentname+'.%s' % (module_name)
	# 一个模块经常变化就可以使用 __import__() 来动态载入。
	# 相当于导入module_name下的__init__.py文件
        module = __import__(module_name, globals=globals(), fromlist=['KEYWORDS'])
	# 初始化中包含KEYWORDS = ['xampp', ] 和rules函数
	# print "__load_keywords:module.KEYWORDS:%s, componentname:%s"%(module.KEYWORDS, componentname)
        return module.KEYWORDS, componentname

    @classmethod
    def __load_rules(self,componentname, module_name):
        module_name = componentname+'.%s' % (module_name)
        module = __import__(module_name,globals=globals(), fromlist=['rules'])
	# print "__load_rules:module.RULES:%s, componentname:%s"%(module.rules, componentname)
        return module.rules,componentname    

    def __load_component_detail_info(self,module_name='',componentname='',func=None,params=None,text=''):
        try:
            params[module_name] = func(componentname,module_name)
#	    module_name: 不同插件下的名称, 如component
#	    self.logger.info('Module '+text+': %s -> %s', module_name, self.keywords[module_name])
        except Exception,e:
            print e
            params[module_name] = [],componentname
#	    self.logger.info('Module '+text+': %s -> None', module_name)
            pass

    def __load_component_detail_plugins(self, componentname=''):
        modules_list = self.__get_component_detail_list(componentname)

        for module_name in modules_list:
            self.components[componentname][module_name] = []
            for plugin_name in self.__get_component_plugins_list(componentname,module_name):
		# component.xampp, XAMPP_0513e4ffc8bbb2129805b3ac0e9545ea
                P = self.__load(componentname+'.%s' % module_name, plugin_name)
                self.components[componentname][module_name].append(P)
		# 加载的__load_xxx获取对应的xxx，在params中使用
                self.__load_component_detail_info(module_name=module_name,componentname=componentname,func=self.__load_keywords,params=self.keywords,text='keywords')
                self.__load_component_detail_info(module_name=module_name,componentname=componentname,func=self.__load_rules,params=self.rules,text='rules')

    def __load_component_plugins(self, modules_list):
        for module_name in modules_list:
            self.components[module_name] = {}
            self.__load_component_detail_plugins(module_name)

    def loader(self):
        self.components = {}
	# load module’s name[middileware,database,...]
        self.__load_component_plugins(map(lambda module_info: module_info['module_name'], self.modules_list))
	# self.logger.info('**************************vuldect loader done!!!**************************')

    def env_init(self, head='',context='',ip='',port='',productname=None,keywords='',nmapscript='',defaultpoc=''):
        self.init(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,nmapscript=nmapscript,defaultpoc=defaultpoc)

    def __match_modules_by_poc(self,head='',context='',ip='',port='',productname=None,keywords='',defaultpoc=''):
        matched_modules = set()
        othermodule=[]

	# 依次遍历组件名components[componentname][module_name] = P()
        for components_name in self.components.keys():
            for module_name in self.components[components_name].keys():
                if module_name in defaultpoc:
                    matched_modules.add((module_name,components_name))

        return matched_modules, othermodule

    def init(self,  head='',context='',ip='',port='',productname=None,keywords='',nmapscript='', defaultpoc='',**kw):
        POCS = []
        modules_list = []

        if defaultpoc == '':
            modules_list, _ = self.__match_modules_by_info(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,hackresults=nmapscript)
        else:
            modules_list, _ = self.__match_modules_by_poc(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,defaultpoc=defaultpoc)
        # set([('http', 'basemodel'), ('tomcat', 'middileware'), ('struts', 'component'), ('apache', 'middileware')])
        if len(modules_list) > 0:
            self.logger.debug('%s:%s 匹配到的可能组件:%s', ip, str(port), str(modules_list))
        for modules, conponent in modules_list:
            for item in self.components[conponent][modules]:
                P = item()
                try:
		            # 没写，现在都返回true
                    if self.__match_rules(pocclass=P,head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,hackresults=nmapscript, **kw):
                        POCS.append(P)
                except Exception,e:
                    self.logger.error('error: %s', e)
#                self.logger.info('Init Plugin: %s', item)
#        self.logger.debug('%s:%s 要执行筛选的组件: %s', ip, str(port), str(POCS))
	    # 执行每个组件下的verify函数，验证是否存在漏洞，区别在于payload不同
        self.match_POC(head=head, context=context, ip=ip, port=port, productname=productname, keywords=keywords,
                       nmapscript=nmapscript, POCS=POCS, **kw)

    @classmethod
    def match_POC(self,head='',context='',ip='',port='',productname=None,keywords='',nmapscript='',POCS=None, **kw):
        haveresult=False
        dataresult=[]
        result={}
        i=0
        email_msg = ''
        for poc in POCS:
            try:
                result = poc.verify(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,hackresults=nmapscript)
                # print type(result), str(result)
                # 默认result['result']=False
                if isinstance(result, dict):
                    if result['result']:
                        i = 1
                        dataresult.append(result['VerifyInfo'])
                        # print (i, "%s:%s存在【%s %s】风险"%(ip, port, result['VerifyInfo']['type'],result['VerifyInfo']['level']))
                        # logger.warning("%s:%s存在【%s %s】风险", (ip, port, result['VerifyInfo']['type'],result['VerifyInfo']['level']))
                        if any(level in str(result['VerifyInfo']['level']) for level in ["HOLE", "WARNING", "NOTE", "INFO"]): 
                            email_msg += """%s:%s存在【%s %s】风险，请及时处理！<br>""" %(ip, port, result['VerifyInfo']['type'],result['VerifyInfo']['level'])
                            callbackresult.sendemail('http://' + ip + ':' + port, email_msg)
                            cprint('http://' + ip + ':' + port + '存在【' + result['VerifyInfo']['type'] + result['VerifyInfo']['level'] + '】风险', 'red')
                else:
                    pass
            except Exception, e:
                print str(poc) + ' verify failed!->' + str(e.message)
        if i > 0:
            callbackresult.storedata(ip=ip,port=port,hackresults=dataresult)
            pass
        del POCS

    @classmethod
    def __match_rules(self,pocclass=None,head='',context='',ip='',port='',productname=None,keywords='',hackresults='', **kw):
	# 每个插件下的T类函数, 目前没有内容，只是返回true, 可以提前对每个组件加一个规则过滤条件
        return pocclass.match_rule(head='',context='',ip='',port='',productname=productname,keywords='',hackresults='', **kw)

    def __match_modules_by_info(self,head='',context='',ip='',port='',productname=None,keywords='',hackresults=''):
        matched_modules = set()
        othermodule=[]
#         for module_name in self.components.keys():
#             othermodule.extend(self.components[module_name].keys())
        if (productname is not None and productname.get('productname',None) is None):
            productname['productname']=''
        if head == None:
            head = ''
        if hackresults == None:
            hackresults = ''

        kw = keywords#关键词(ssh.mysql,rsync.ftp)
        for module_name, module_info in self.keywords.items():
            modulekeywords = module_info[0]
            componentname = module_info[1]
#	    modulekeywords:['xampp'], componentname:component
#	    print "__match_modules_by_info modulekeywords:%s, componentname:%s"%(str(modulekeywords), str(componentname))
            if not modulekeywords:
	    	print "__match_modules_by_info modulekeywords is NULL.matched_modules.add((%s,%s))"%(str(module_name), str(componentname))
                matched_modules.add((module_name,componentname))
                continue
            for keyword in modulekeywords:
#	 	组件在产品名、头部或者nmapscript(这里命名有问题，hackresults->nmapscript)信息中出现，均应当作危险信息进行检测验证
	    	if keyword in kw or keyword in productname.get('productname','').lower()  or keyword in head.lower() or keyword in str(hackresults).lower():
                    self.logger.info('Match Keyword: -> %s', keyword)
                    matched_modules.add((module_name,componentname))
                    break
        for module_name, module_info in self.rules.items():
            rules = module_info[0]
            componentname = module_info[1]
#	    <function rules at 0x7fea340322a8>, componentname:component
#	    print "__match_modules_by_info modulerules:%s, componentname:%s"%(str(rules), str(componentname))
            if not rules:
                matched_modules.add((module_name,componentname))
                self.logger.info('Match Rules: -> %s', module_name)
                continue
#	    相应组件关键词在context中/productname/head等init函数中定义的规则满足，则返回true
            if rules(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,hackresults=''):
                self.logger.info('Match Rules: -> %s', keyword)
                matched_modules.add((module_name,componentname))
        return matched_modules, othermodule

    def detect(self, head='',context='',ip='',port='',productname={},keywords='',nmapscript='',defaultpoc=''):
        # print ("detection::vuldetect::plugins::default()\n\nhead[%s]\nip[%s]\nport[%s]\nproductname[%s]\nkeywords[%s]\nhackresults[%s]\ndefaultpoc[%s]\n"%(str(head),str(ip),str(port),str(productname),str(keywords),str(hackresults),str(defaultpoc)))
#	形式components[componentname][module_name] = P()
#	self.logger.info('now the source component: %s', self.components)
        if self.components=={} or self.keywords == {} or self.rules=={}:
            self.loader()
        self.env_init(head=head,context=context,ip=ip,port=port,productname=productname,keywords=keywords,nmapscript=nmapscript,defaultpoc=defaultpoc)
        return

if __name__ == "__main__":
    a = PocController()
