KEYWORDS = ['struts', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'struts2' in context or '.action'  in context or '.do'  in context:
        return True
    else:
        return False
    

