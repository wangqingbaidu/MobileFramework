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
    
    nInputPlane = -1
    
    def __init__(self, nOutputPlane):
        self.nOutputPlane = nOutputPlane
    
    @property
    def vertexShader(self):        
        print 'Please complete the function of getting vertexShader.'
        assert None
    
    @property
    def fragmentShader(self):                
        print 'Please complete the function of getting fragmentShader.'
        assert None
    
    def toDict(self):
        print 'Please complete this function: toJson'
        assert None
    
    def resize(self, iw, ih, ic):
        print 'Please complete this function: resize'
        assert None
        