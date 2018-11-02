KEYWORDS = ['netsurveillance', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if int(port) in [81] or 'xmeye' in context.lower() or 'netsurveillance' in hackresults.lower():
        return True
    else:
        return False
