KEYWORDS = ['jboss', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'youcandoit.jpg' in context or 'JBossWeb'in context or 'jboss' in hackresults or 'jboss' in head :
        return True
    else:
        return False