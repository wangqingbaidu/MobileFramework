# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月22日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
mapping = {
    'darknet':{
        'nOutputPlane':'filters',
        'kW':'size',
        'kH':'size',
        'dW':'stride',
        'dH':'stride',
        'padW':'pad',
        'padH':'pad',
        'activation':'activation',
        'weights':'weights',
        'bias':'bias'
        }
    }
def getFrameworkAttribute(key, framework='darknet'):
    if mapping.has_key(framework) and mapping[framework].has_key(key):
        return mapping[framework][key]
    else:
        print 'Got key error %s %s' %(framework, key)
        return None
    