#!/usr/bin/python
#coding:utf-8

import traceback
import gc,objgraph

def identify_main(head='',context='',ip='',port='',productname='',protocol='',nmapscript=''):
    keywords=''
    hackresults=''
#     print '运行前状态'
#     gc.collect()
#     objgraph.show_growth()
    print "detection::page_identify::identify_main()", ip + ":" + port,'正在纳入检测的队列'
    try:
        # from httpdect import headdect	#webdetection缺失
        from fluzzdetect import fuzztask    # 只给了这部分代码, 检测拼接的子url和父url
        from vuldect import pocsearchtask
        # 通过webdetection获取webinfo，hackresults为空
        # keywords, hackresults = headdect.dect(head=head, context=context, ip=ip, port=port, protocol=protocol)
        print "\n\ndetection::page_identify::identify_main() fuzztask begin detect...."
        fuz = fuzztask.getObject()
        fuz.add_work([(head,context,ip,port,productname,keywords,nmapscript,protocol)])

        print "\n\ndetection::page_identify::identify_main() pocsearchtask begin init...."
#        print ("detection::vuldetect::head[%s]\nip[%s]\nport[%s]\nproductname[%s]\nkeywords[%s]\nnmapscript[%s]\nprotocol[%s]\n"%(str(head),str(ip),str(port),str(productname),str(keywords),str(nmapscript),str(protocol)))
        temp = pocsearchtask.getObject()
        print "\n\ndetection::page_identify::identify_main() pocsearchtask begin detect...."
        temp.add_work([(head,context,ip,port,productname,keywords,nmapscript,protocol)])
    except Exception ,e:
        print traceback.print_exc()
        pass
    gc.collect()
    objgraph.show_growth()
    print '检测运行后状态'

    return keywords, hackresults

# from fluzzdetect import fuzztask

# fuz = fuzztask.getObject()
# fuz.add_work([('head','context','113.105.74.144','80','productname','keywords','nmapscript','http')])
# print a.scanvul(ip='113.105.74.144',port='80',protocal='http')
