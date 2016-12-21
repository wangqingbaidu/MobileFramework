# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月21日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
from glnn.BaseLayer import BaseLayer
class SpatialPadding(BaseLayer):
    __vertexShader = None
    __fragmentShader = None
    
    def __init__(self, padW, padH):
        self.padW = padW
        self.padH = padH
    
    @property
    def vertexShader(self):
        pass
    
    @property
    def fragmentShader(self):
        pass
    
    def toJson(self):
        pass
    
    def resize(self, iw, ih, ic):
        pass
    
    def __parserVertexShader(self):
        pass
    
    def __parserFragmentShader(self):
        pass