KEYWORDS = ['mongo', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if '27017' in port :
        return True
    else:
        return False