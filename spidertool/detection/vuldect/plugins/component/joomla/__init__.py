KEYWORDS = ['joomla', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'joomla' in context or 'joomla' in hackresults:
        return True
    else:
        return False
