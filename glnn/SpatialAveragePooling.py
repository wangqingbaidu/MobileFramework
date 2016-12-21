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
import math
class SpatialAveragePooling(BaseLayer):
    """
    glsl to be done!
    """
    
    __vertexShader = None
    __fragmentShader = None
    
    def __init__(self,
                 kW,
                 kH,
                 dW = 1,
                 dH = 1,
                 padW = None,
                 padH = None,):
        self.kW = kW
        self.kH = kH
        self.dW = dW
        self.dH = dH
        
        self.padW = padW if padW != None else (kW - 1) / 2
        self.padH = padH if padH != None else (kH - 1) / 2
    
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
    
    def resize(self, iw, ih, ic):
        self.nInputPlane = self.nOutputPlane = ic
        self.inputWidth = iw
        self.inputHeight = ih
        self.__computeOutputSize()
        
        self.__parserVertexShader()
        self.__parserFragmentShader()
        
    def toJson(self):
        pass
    
    def __parserVertexShader(self):
        pass
    
    def __parserFragmentShader(self):
        pass
    
    def __computeOutputSize(self):
        if self.inputWidth and self.inputHeight:
            self.outputWidth = (self.inputWidth + 2 * self.padW - self.kW) / self.dW + 1
            self.outputHeight = (self.inputHeight + 2 * self.padH - self.kH) / self.dH + 1
            
        group = self.nOutputPlane / 4 + (1 if self.nOutputPlane % 4 else 0)
        self.blockX = int(math.sqrt(group))
        if group % self.blockX == 0:
            self.blockY = group / self.blockX
            self.if_condition = False
        else:
            self.blockY = group / self.blockX + 1
            self.if_condition = True