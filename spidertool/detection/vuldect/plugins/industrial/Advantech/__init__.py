KEYWORDS = ['Advantech', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if int(port) in [232,422,485] or 'advantech' in context.lower():
        return True
    else:
        return False
