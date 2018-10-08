KEYWORDS = ['cgi', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    
    
    if 'cgi-bin' in hackresults or 'cgi-bin' in  context:
        return True
    else:

        return False