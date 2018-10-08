KEYWORDS = ['redis', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):


    if int(port) in [6379] or productname.get('protocol','') in ['redis']:
        return True
    else:

        return False