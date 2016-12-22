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
from utils import getShader
import json
from utils.obj2dict import obj2dict
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
    
    def toDict(self):
        return obj2dict(self)
    
    def resize(self, iw, ih, ic):        
        self.inputWidth = iw
        self.outputWidth = iw + 2 * self.padW
        self.inputHeight = ih
        self.outputHeight = ih + 2 * self.padH
        self.nOutputPlane = self.nInputPlane = ic
        
        self.__parserVertexShader()
        self.__parserFragmentShader()
    
    def __parserVertexShader(self):
        self.__vertexShader = getShader.getVertexShader(self)
    
    def __parserFragmentShader(self):
        self.__fragmentShader = getShader.getFragmentShader(self)
        
if __name__ == '__main__':
    padding = SpatialPadding(1,1)
    padding.resize(4, 4, 4)
    print dir(padding)
    print padding.fragmentShader