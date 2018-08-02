#!/usr/bin/python
#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from spidertool import webtool, config
from ..control import taskscontrol, taskcontrol, jobcontrol

import json

localconfig = config.Config

def indexpage(request):
    now = datetime.datetime.now()
    return render_to_response('index.html', {'current_date': now})

def showtask(request):
    now = datetime.datetime.now()
    username = request.COOKIES.get('username','未知')
    return render_to_response('nmaptoolview/taskmain.html', {'username':username})

def taskquery(request):
    islogin = request.COOKIES.get('islogin',False)
    username = request.POST.get('username','')
    page = request.POST.get('page','0')
    response_data = {}
    response_data['result'] = '0'
    response_data['page'] = page

    if islogin:
        response_data['result'] = '1'
        # tasks: a json array, collect all task info; taskcount: 任务数; pagecount: 页面数量
        tasks, taskcount, pagecount = taskscontrol.taskshow(username=username, page=page)
        response_data['length'] = taskcount
        response_data['jobs'] = tasks
        response_data['pagecount'] = pagecount
        return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")
    else:
        return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")

def addtask(request):
    islogin = request.COOKIES.get('islogin', False)
    username = request.COOKIES.get('username', '')
    response_data = {}
    response_data['result'] = '0'
    if islogin == False:
        print '未登录'
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                            content_type="application/json")
    #当job的name和address不为空的时候则通过post形式获取job信息，初始化job对象
    job, result = taskscontrol.loadtask(request, username=username)

    if result == False:
        print '作业不完善'
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                            content_type="application/json")

    result = taskscontrol.addtask(job)
    # save ip, a iptask.object
    temp = taskscontrol.createjob(job)

    if result:
        print '==========================addtask()==添加job操作成功, set response_data["result"]=1'
        response_data['result'] = '1'
    return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                        content_type="application/json")
# 启动任务 state = 3
def starttask(request):
    data = updatejob(request, state='3')
    return HttpResponse(json.dumps(data,skipkeys=True,default=webtool.object2dict), content_type="application/json")

# 暂停任务 state = 4
def pausetask(request):
    data = updatejob(request, state='4')
    return HttpResponse(json.dumps(data, skipkeys=True, default=webtool.object2dict), content_type="application/json")

# 销毁任务 state = 6
def destorytask(request):
    data = updatejob(request, state='6')
    return HttpResponse(json.dumps(data, skipkeys=True, default=webtool.object2dict), content_type="application/json")

# 更新任务
"""
1 未启动
2 排队中
3 正在进行
4 挂起
5 完成
6 终止

mode:
0 异常
1 正常
"""
def updatejob(request, state=''):
    print ("===============================================================================\n======================tasks state:%s request.method:%s======================\n\n"%(state, request.method))
    if request.method=='POST':   # POST
        islogin = request.COOKIES.get('islogin', False)
        jobid= request.POST.get('taskid','')
        # jobid= request.POST.get('taskid','14032678-90ac-11e8-af6f-74e50ba386da')
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
        # return render(request, 'nmptoolview/post.html', ctx)

        # 开始操作tasksdata表，执行对应的状态操作
        if state == '3':
            tempresult = taskscontrol.jobupdate(jobstatus=state, username=username, taskid=jobid, completenum='0')
        # elif  state=='4':
        #     pass
        else:
            if role=='1':
                tempresult=taskscontrol.jobupdate(jobstatus=state,username=username,taskid=jobid)
#             print 'this is user'
            else:
                tempresult=taskscontrol.jobupdate(jobstatus=state,taskid=jobid)
        if tempresult == True:
            tasks, count, pagecount = taskscontrol.taskshow(username=username, page='0',taskid=jobid)
            table = localconfig.taskstable
            print ('\n%s更新成功, 总数为:%s页数为:%d'%(table, count, pagecount))

            if count > 0:
                tasktotally = taskcontrol.getObject()
                task = tasks[0] # a Job object
                # 更新job(taskdata表)
                if state == '3':
                    jobcontrol.jobupdate(jobstatus='2', groupid=jobid)
                    taskscontrol.startjob(task) # 和createjob中的用法一致, 区别在哪？巍峨和不直接用createjob
                    # tasktotally.add_work(jobs)
                else:
                    jobcontrol.jobupdate(jobstatus=state, groupid=jobid)
                # page=page+1
            response_data['result'] = '1'
        return response_data

