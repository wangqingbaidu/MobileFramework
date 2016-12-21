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
        if not self.__vertexShader:
            self.__parserVertexShader()
        return self.__vertexShader
    
    @property
    def fragmentShader(self):
        if not self.__fragmentShader:
            self.__parserFragmentShader()
        return self.__fragmentShader
    
    def toJson(self):
        pass
    
    def resize(self, iw, ih, ic):
        pass
    
    def __parserVertexShader(self):
        pass
    
    def __parserFragmentShader(self):
        pass