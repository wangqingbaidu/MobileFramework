# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
class BaseLayer:    
    inputWidth = None
    inputHeight = None
    outputWidth = None
    outputHeight = None
    
    vertexShader = None
    fragmentShader = None
    
    def __init__(self,
                 nInputPlane,
                 nOutputPlane):
        self.nInputPlane = nInputPlane
        self.nOutputPlane = nOutputPlane
    
    def getVertexShader(self):        
        print 'Please complete this function: getVertexShader'
        assert None
        
    def getFragmentShader(self):                
        print 'Please complete this function: getFragmentShader'
        assert None
    
    def toJson(self):
        print 'Please complete this function: toJson'
        assert None
        
        