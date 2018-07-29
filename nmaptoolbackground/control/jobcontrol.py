#!/usr/bin/python
#coding:utf-8
from spidertool import SQLTool ,config
from ..model import job


limitpage=15


localconfig=config.Config()
def jobshow(jobname = '',jobstatus = '',username = '',taskid = '',jobport = '',result = '',page='0',groupid = '',jobaddress = ''):
    validresult=False
    request_params=[]
    values_params=[]
	# formatstring: return '\''+str+'\''
    tmp = ""
    if groupid != '':
        tmp += ' groupid ' + groupid
        request_params.append('groupsid')
        values_params.append(SQLTool.formatstring(groupid))
    if jobname != '':
        tmp += ' taskname ' + jobname
        request_params.append('taskname')
        values_params.append(SQLTool.formatstring(jobname))
    if jobstatus != '':
        tmp += ' taskstaus ' + taskstaus
        request_params.append('taskstatus')
        values_params.append(SQLTool.formatstring(jobstatus))
    if username != '':
        tmp += ' username ' + username
        request_params.append('username')
        values_params.append(SQLTool.formatstring(username))
    if taskid != '':
        tmp += ' taskid ' + taskid
        request_params.append('taskid')
        values_params.append(SQLTool.formatstring(taskid))
    if jobport != '':
        tmp += ' taskport ' + taskport
        request_params.append('taskport')
        values_params.append(SQLTool.formatstring(jobport))
    if jobaddress  !=  '':
        tmp += ' taskaddress ' + jobaddress
        request_params.append('taskaddress')
        values_params.append(SQLTool.formatstring(jobaddress))

    print ("======================jobshow: %s======================"%tmp)
    DBhelp = SQLTool.DBmanager()
    DBhelp.connectdb()
    table = localconfig.tasktable   #taskdata
    result, content, count, col = DBhelp.searchtableinfo_byparams([table], ['count(*)'], request_params, values_params)

    if count > 0:
        count = int(result[0]['count(*)'])
    if count == 0:
        pagecount = 0;
    elif count % limitpage> 0:
#         pagecount = math.ceil(count / limitpage)
        pagecount=int((count+limitpage-1)/limitpage) 
    else:
        pagecount = count / limitpage

    print ("======================DBhelp.searchtableinfo_byparams() pagecount=%d======================"%pagecount)

    if pagecount > 0:
        limit = ' limit ' + str(int(page)*limitpage) + ',' + str(limitpage)
        # 数据库查询结果，内容，多少个结果，多少列（这里定义的第二个参数个数）
        result, content, count, col = DBhelp.searchtableinfo_byparams([table], ['username','taskid','taskname','taskprior','taskstatus','starttime','taskaddress','taskport','result','endtime','createtime','forcesearch','groupsid'], request_params, values_params, limit, order='createtime desc')

        DBhelp.closedb()
        jobs=[]
        if count > 0:
            validresult=True
            for temp in result :
                ajob = job.Job(username=temp['username'],jobid=temp['taskid'],jobname=temp['taskname'],priority=temp['taskprior'],jobstatus=temp['taskstatus'],starttime=temp['starttime'],jobaddress=temp['taskaddress'],jobport=temp['taskport'],result=temp['result'],endtime=temp['endtime'],createtime=temp['createtime'],forcesearch=temp['forcesearch'],groupsid=temp['groupsid'])

#                 ajob = job.Job(username=temp[0],jobid=temp[1],jobname=temp[2],priority=temp[3],jobstatus=temp[4],starttime=temp[5],jobaddress=temp[6],jobport=temp[7],result=temp[8],endtime=temp[9],createtime=temp[10],forcesearch=temp[11])
                jobs.append(ajob)
        return jobs, count, pagecount

    return [],0,pagecount

##count为返回结果行数，col为返回结果列数,count,pagecount都为int型
def loadjob(request, username = ''):
    jobname = request.POST.get('jobname','')
    jobaddress = request.POST.get('jobaddress','')
    jobport = request.POST.get('jobport','')
    priority = request.POST.get('priority','1')
    abstract = request.POST.get('abstract','')
    forcesearch = request.POST.get('forcesearch','0')
    tempjob = None

    if jobaddress == '' or jobname == '':
        return tempjob, False
    tempjob = job.Job(jobname = jobname,jobaddress = jobaddress,priority=priority, username=username,jobport = jobport,forcesearch=forcesearch)
    return tempjob, True

def jobadd(job):
    jobname = job.getJobname()
    jobaddress = job.getJobaddress()
    jobport = job.getPort()
    priority = job.getPriority()
    jobstatus = job.getStatus()
    username = job.getUsername()
    starttime = job.getStarttime()
    createtime = job.getCreatetime()
    taskid = job.getJobid()
    result = job.getResult()
    groupsid = job.getGroupsid()
    forcesearch = job.getForcesearch()

    print ('======================jobadd forcesearch is %s======================'%forcesearch)

    request_params = []
    values_params = []
    if groupsid  !=  '':
        request_params.append('groupsid')
        values_params.append(groupsid)
    if createtime  !=  '':
        request_params.append('createtime')
        values_params.append(createtime)
    if starttime  !=  '':
        request_params.append('starttime')
        values_params.append(starttime)
    if jobaddress  !=  '':
        request_params.append('taskaddress')
        values_params.append(jobaddress)
    if priority  !=  '':
        request_params.append('taskprior')
        values_params.append(priority)
    if jobname  !=  '':
        request_params.append('taskname')
        values_params.append(jobname)
    if jobstatus  !=  '':
        request_params.append('taskstatus')
        values_params.append(jobstatus)
    if username  !=  '':
        request_params.append('username')
        values_params.append(username)
    if taskid  !=  '':
        request_params.append('taskid')
        values_params.append(taskid)
    if jobport  !=  '':
        request_params.append('taskport')
        values_params.append(jobport)
    if result  !=  '':
        request_params.append('result')
        values_params.append(result)
    if forcesearch  !=  '':
        request_params.append('forcesearch')
        values_params.append(forcesearch)        

    table = localconfig.tasktable   #taskdata
    DBhelp = SQLTool.DBmanager()
    DBhelp.connectdb()

    tempresult = DBhelp.inserttableinfo_byparams(table=table, select_params=request_params, insert_values = [tuple(values_params)])

    DBhelp.closedb()

    return tempresult

def jobgetwork():
    pass

def jobupdate(taskid = '',jobport = '',jobaddress = '',jobname = '',priority = '',jobstatus = '',starttime = '',result = '',username = '',finishtime = '',groupid = ''):
    request_params=[]
    values_params=[]
    wset_params=[]
    wand_params=[]

    if starttime != '':
        request_params.append('starttime')
        values_params.append(SQLTool.formatstring(starttime))
    if finishtime != '':
        request_params.append('endtime')
        values_params.append(SQLTool.formatstring(finishtime))
    if jobaddress != '':
        request_params.append('taskaddress')
        values_params.append(jobaddress)
    if priority != '':
        request_params.append('taskprior')
        values_params.append(priority)
    if jobname != '':
        request_params.append('taskname')
        values_params.append(jobname)
    if jobstatus != '':
        request_params.append('taskstatus')
        values_params.append(jobstatus)
    if jobport != '':
        request_params.append('taskport')
        values_params.append(jobport)
    if result != '':
        request_params.append('result')
        values_params.append(result)

    if username != '':
        wset_params.append('username')
        wand_params.append(SQLTool.formatstring(username))
    if taskid != '':
        wset_params.append('taskid')
        wand_params.append(SQLTool.formatstring(taskid))
    if groupid != '':
        wset_params.append('groupsid')
        wand_params.append(SQLTool.formatstring(str(groupid)))

    table = localconfig.tasktable #taskdata

    DBhelp = SQLTool.DBmanager()
    DBhelp.connectdb()

    tempresult=DBhelp.updatetableinfo_byparams([table],request_params,values_params,wset_params,wand_params)
    DBhelp.closedb()

    return tempresult

    
