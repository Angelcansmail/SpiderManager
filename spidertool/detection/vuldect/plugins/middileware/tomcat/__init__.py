KEYWORDS = ['tomcat', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'Apache Tomcat' in context or 'tomcat' in head.lower() or 'tomcat' in context.lower() or 'tomact' in productname.get('productname', ''):
        return True
    else:
        return False
