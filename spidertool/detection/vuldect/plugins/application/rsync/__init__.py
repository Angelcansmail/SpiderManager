KEYWORDS = ['rsync', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):


    if int(port) in [873] or productname.get('protocol','') in ['rsync']:
        return True
    else:

        return False