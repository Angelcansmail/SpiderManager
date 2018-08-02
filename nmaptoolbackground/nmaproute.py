#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from model.user import User
from control import usercontrol, jobcontrol, taskcontrol, ipcontrol, portcontrol

from spidertool import webtool, config, Sqldatatask, Sqldata, connectpool, sniffertask
localconfig = config.Config()

# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators import csrf
import json

# 用户注册
def sigin(request):
   if request.method  ==  'GET':
       return render_to_response('nmaptoolview/sigin.html', {'data':''})

# 用户登录--成功登录后跳转到taskmain.html界面
def login(request):
    if request.method  ==  'GET':
        return render_to_response('nmaptoolview/login.html', {'data':''})
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

		# result = Ture/False(if len(col) > 0);
        result, username, role, power = usercontrol.validuser(username, password)

        ctx = {}
        ctx['username'] = username
        ctx['password'] = password
        ctx['result'] = result
        ctx['role'] = role
        ctx['power'] = power

        # return render(request, 'nmaptoolview/post.html', ctx)
        # return render(request, 'nmaptoolview/taskmain.html', {'data': '用户名和密码正确', 'username':username})
        if result:
            # 在base/navbar.html模板中使用username参数
            response = render(request, 'nmaptoolview/taskmain.html', {'data': '用户名和密码正确', 'username':username})
            # 将username写入浏览器cookie,失效时间为3600
            loginuser = User(result, username, password, role, power)
            webtool.setCookies(response, loginuser, 3600)
            return response
        else:
            return render(request, 'nmaptoolview/login.html', {'data': '用户名和密码错误'})

# 注销登录
def logout(request):
    response= render_to_response('nmaptoolview/login.html', {'data':''})
    webtool.delCookies(response)
    return response

# 用户信息查看
def userinfo(request):
    return render_to_response('nmaptoolview/userinfo.html', {'data':''})


#a function to redirect to main page               
def indexpage(request):
    islogin = request.COOKIES.get('islogin',False)
    username = request.COOKIES.get('username','')

    if islogin:
        return render_to_response('nmaptoolview/taskmain.html',{'username':username})
    return render_to_response('nmaptoolview/login.html', {'data':''})

# 获取组类目信息
def groupitem(request):
    islogin = request.COOKIES.get('islogin', False)
    username = request.COOKIES.get('username','')
    groupid = request.GET.get('groupid','')  #groupid哪里赋值的 tasksid(tasksdata表)
    print ("======================groupitem(groupid:%s)======================"%groupid)

    if islogin:
        return render_to_response('nmaptoolview/mainpage.html',{'username':username,'groupid':groupid})
    return render_to_response('nmaptoolview/login.html', {'data':''})

#a function to get the port information of IP
def taskdetail(request):
    if request.method == 'GET':
        islogin = request.COOKIES.get('islogin',False)
        # jobid应该自动获取，不是手动赋值，仅为测试！！
        jobid = request.GET.get('jobid','1410a6d6-90ac-11e8-af6f-74e50ba386da')
        # jobid = request.GET.get('jobid','')
        username = request.COOKIES.get('username','')
        role = request.COOKIES.get('role','1')

        ctx = {}
        ctx['islogin'] = islogin
        ctx['jobid'] = jobid
        ctx['username'] = username
        ctx['role'] = role

        # return render_to_response('nmaptoolview/post.html', ctx)

        # jobs: 返回的数据库结果, count:多少个结果, pagecount:页面数
        if islogin == False:
            return render_to_response('nmaptoolview/login.html', {'data':''})
        # 数据库表中原始存在的数据一定是管理员建立的，role初始化非1,因此role!=1一定是普通的用户，注册都设置为1
        if role == '1':
            jobs, count, pagecount = jobcontrol.jobshow(username = username, taskid = jobid)
        else:
            jobs, count, pagecount = jobcontrol.jobshow(taskid=jobid)
        if count > 0 and jobid != '':
            return render_to_response('nmaptoolview/taskdetail.html', {'taskid':jobid, 'username':username})
        else:
            return HttpResponse("权限不足或者没有此任务")

# 显示任务信息
def jobshow(request):
    islogin = request.COOKIES.get('islogin',False)
    username = request.POST.get('username','')
    page = request.POST.get('page','0')
    groupid = request.POST.get('groupid', '')

    response_data = {}  
    response_data['result'] = '0' 
    response_data['page'] = page

    if islogin:
        response_data['result'] = '1' 
        jobs, count, pagecount = jobcontrol.jobshow(username=username, page=page, groupid=groupid)
        response_data['length'] = count
        response_data['jobs'] = jobs
        response_data['pagecount'] = pagecount
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict), content_type="application/json")
    else:
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict), content_type="application/json")

# 任务添加功能
def addjob(request):
    islogin = request.COOKIES.get('islogin',False)
    username = request.COOKIES.get('username','')
    response_data = {}  
    response_data['result'] = '0' 

    if islogin == False:
        print '未登录'
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict), \
                content_type="application/json")  
    # 扫描地址或者端口不为空，就对填写的job信息进行获取，并初始化job对象, result=True
    job, result = jobcontrol.loadjob(request, username=username)

    if result == False:
        print '信息不完善（请检查扫描地址和端口信息，重新添加）'
        return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  
 
    result = jobcontrol.jobadd(job)
    print "==========================debug::jobadd()==========================", result
    if result:
        print '操作成功'
        response_data['result'] = '1' 
    return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  

# 任务启动
def startjob(request):
    data = updatejob(request, state='2')
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  

# 任务挂起
def pausejob(request):
    data = updatejob(request, state='4')
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  

# 终止任务
def destroyjob(request):
    data = updatejob(request, state='6')
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  

# 更新任务
"""
status
1 未启动
2 排队中
3 正在进行
4 挂起
5 完成
6 终止
"""
def updatejob(request,state=''):
    print ("==========================================================================\n======================job state:%s request.method:%s======================\n==========================================================================\n"%(state, request.method))
    if request.method=='POST':   #POST
        islogin = request.COOKIES.get('islogin', False)
        jobid = request.POST.get('taskid','')
        # jobid = request.POST.get('taskid','1410a6d6-90ac-11e8-af6f-74e50ba386da')
        username = request.COOKIES.get('username','') 
        role = request.COOKIES.get('role','1')
        response_data = {}  
        response_data['result'] = '0'

        ctx = {}
        ctx['islogin'] = islogin
        ctx['jobid'] = jobid
        ctx['username'] = username
        ctx['role'] = role
        ctx['state'] = state
        # return render(request, 'nmaptoolview/post.html', ctx)

        if role == '1':
            tempresult = jobcontrol.jobupdate(jobstatus=state, username=username, taskid=jobid)
            print 'this is user'
        else:
            tempresult = jobcontrol.jobupdate(jobstatus=state, taskid=jobid)

        if tempresult == True:
            if state=='2':
                jobs, count, pagecount = jobcontrol.jobshow(taskid=jobid)

                if count > 0:
                    tasktotally = taskcontrol.getObject()
                    if jobs[0].getForcesearch == 1:
                        tasktotally.add_work(jobs)
                    else:
                        tasktotally.add_work(jobs)
            response_data['result'] = '1'
        return response_data
    
# jobcontrol.getIP(jobs)
# a function to get the job of user
def ipmain(request):   
    if request.method=='POST':  #POST
        islogin = request.COOKIES.get('islogin',False)
        jobid= request.POST.get('taskid','')
        # jobid = request.POST.get('taskid','1410a6d6-90ac-11e8-af6f-74e50ba386da')
        page = request.POST.get('page','0')
        username = request.COOKIES.get('username','') 
        role = request.COOKIES.get('role','1')
        response_data = {}  
        response_data['result'] = '0' 

        # 从ip_maindata表中，根据条件过滤信息，表内容什么时候写入的?
        if role=='1':
            jobs, count, pagecount = jobcontrol.jobshow(username=username, taskid=jobid)
            print 'this is user, jobid=', jobid
        else:
            jobs, count, pagecount = jobcontrol.jobshow(taskid=jobid)
            print 'this is administor, jobid=', jobid

        if count > 0 and jobid != '':
            ip = jobs[0].getJobaddress()   
            port = jobs[0].getPort()
            jobstatuss = jobs[0].getStatus()
            isip = webtool.isip(ip) #xxx.xxx.xxx.xxx

            # ips:所有结果存入的一个list中(每个结果都是一个Ip对象) counts:查询到的结果数量, pagecounts:页面数
            if isip:
                ips, counts, pagecounts = ipcontrol.ipshow(ip=ip)
            else:
                ips, counts, pagecounts = ipcontrol.ipshow(hostname=ip)

                if counts > 0:
                    ip = ips[0].getIP()
                else:
                    ip = '未知'
            response_data['result'] = '1' 
            response_data['ipstate'] = '0' 
            response_data['ip'] = ip
            response_data['jobstate'] = jobstatuss
#             print 'it has this task'
            if counts > 0:
                table = localconfig.iptable
                print ('%s has ip:%s'%(table, ip))
                response_data['ipstate'] = '1' 
                response_data['length'] = counts
                response_data['ips'] = ips[0]
                response_data['pagecount'] = pagecounts
                portinfo = portcontrol.divided(port, 'port')    # from a part sql sentence "and (port=xxx/port between a and b or...)"
                # ports为返回的端口信息，存储每个端口的结果（Port对象)
                ports, portcount, portpagecount = portcontrol.portshow(ip=ip, page=page, extra=portinfo)
                response_data['ports'] = ports
                response_data['portslength'] = portcount
                response_data['portspagecount'] = portpagecount
                response_data['portspage'] = page

                return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  
            else:
                return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  
        else:
            return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  

# 上传端口信息
def upload_port_info(request):
    sqldatawork = []
    func = request.POST.get('func','')
    dic = request.POST.get('dic','{}')
    nowdic = eval(dic)
    tempwprk = Sqldata.SqlData(func, nowdic)
    sqldatawork.append(tempwprk)
    sqlTool = Sqldatatask.getObject()
    sqlTool.add_work(sqldatawork)   #把任务添加到进程中

    data={}
    data['result']='1'
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")

# 上传ip信息
def upload_ip_info(request):
    sqldatawork = []
    func = request.POST.get('func','')
    dic = request.POST.get('dic','{}')
    nowdic = eval(dic)  #存在安全隐患, 改用json库
    tempwprk = Sqldata.SqlData(func, nowdic)    #赋值给Sqldata类, 后期通过getXXX获取, 在Sqldatatask.py中
    sqldatawork.append(tempwprk)
    sqlTool = Sqldatatask.getObject()
    sqlTool.add_work(sqldatawork)
    works = request.POST.get('workdetail',[])
    print "nmaproute::upload_ip_info():", works
    temphosts = request.POST.get('ip','')
    tempvendor=request.POST.get('vendor','')
    temposfamily=request.POST.get('osfamily','')
    temposgen=request.POST.get('osgen','')
    tempaccuracy=request.POST.get('accuracy','')
    localtime = str(time.strftime("%Y-%m-%d %X",  time.localtime()))
    temphostname=request.POST.get('hostname','')
    tempstate=request.POST.get('state','')
    ipcontrol.ip_info_upload(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)

    data={}
    data['result']='1'
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")   

# 图表展示
def chartshow(request):
    response= render_to_response('nmaptoolview/chartshow.html', {'data':''})
    return response

#a function to redirect to get the test data from baidu
def chartdata(request):
    httpClient = None
    response_data={}
    try:
#         httpClient = httplib.HTTPConnection('echarts.baidu.com', 80, timeout=30)
#         httpClient.request('GET', '/doc/example/data/migration.json')
        connectpool_t = connectpool.getObject()
        address = 'http://echarts.baidu.com/echarts2/doc/example/data/migration.json'
        head,ans = connectpool_t.getConnect(address)
    #response是HTTPResponse对象
#         response = httpClient.getresponse()
#         print response.status
#         print response.reason
        response_data = ans
        print response_data
    except Exception, e:
        print '接受的数据出现异常'+str(e)
    finally:
        if httpClient:
            httpClient.close()
#         print response_data
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),  content_type="application/json")

#the function below is to use for assign work to other PC   
def getwork(request):
    data={}
    taskinstance = sniffertask.getObject()
    tempwork = taskinstance.get_work()  # ThreadTool.py定义，获取剩余任务，集群操作

    if len(tempwork) > 0:
        data['result'] = '1'
        data['jobs'] = tempwork
    else:
        data['result']='0'
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")   


def systeminfo(request):
    from spidertool import sniffertask, zmaptool, portscantask, Sqldatatask
    from spidertool.detection.fluzzdetect import fuzztask
#    from spidertool.detection.vuldect import pocsearchtask
    resultdata = {}
    # TaskTool中定义的对象信息
    resultdata['nmapfont'] = taskcontrol.getObject().get_length()   # threadtool.getqueue_size()
    resultdata['nmapfont_running'] = taskcontrol.getObject().get_current_task_num() #get_running_size()

    resultdata['nmapback'] = sniffertask.getObject().get_length()   #
    resultdata['nmapback_running'] = sniffertask.getObject().get_current_task_num()

    resultdata['portacsn'] = portscantask.getObject().get_length()
    resultdata['portacsn_running'] = portscantask.getObject().get_current_task_num()

    resultdata['fuzz']=fuzztask.getObject().get_length()
    resultdata['fuzz_running'] = fuzztask.getObject().get_current_task_num()

#    resultdata['pocdect'] = pocsearchtask.getObject().get_length()
#    resultdata['pocdect_running']=pocsearchtask.getObject().get_current_task_num()

    resultdata['sqltask'] = Sqldatatask.getObject().get_length()
    resultdata['sqltask_running']=Sqldatatask.getObject().get_current_task_num()

    return HttpResponse(json.dumps(resultdata,skipkeys=True,default=webtool.object2dict), content_type="application/json")



