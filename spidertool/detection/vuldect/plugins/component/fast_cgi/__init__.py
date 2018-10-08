KEYWORDS = ['fast-cgi', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if port=='9000':
        return True
    else:
        return False