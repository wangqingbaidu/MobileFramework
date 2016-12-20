# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''

from glsl import getShader
from glnn.BaseLayer import BaseLayer
import math

class SpatialConvolution(BaseLayer):
    def __init__(self,
                 nInputPlane,
                 nOutputPlane,
                 kW,
                 kH,
                 dW = 1,
                 dH = 1,
                 padW = None,
                 padH = None):
        BaseLayer.__init__(self, nInputPlane, nOutputPlane)
        self.kW = kW
        self.kH = kH
        self.dW = dW
        self.dH = dH
        self.padW = padW if padW != None else (kW - 1) / 2
        self.padH = padH if padH != None else (kH - 1) / 2
        self.weights = None
        self.bias = None
        group = nOutputPlane / 4 + (1 if nOutputPlane % 4 else 0)
        
        self.blockX = int(math.sqrt(group))
        if group % self.blockX == 0:
            self.blockY = group / self.blockX
            self.if_condition = False
        else:
            self.blockY = group / self.blockX + 1
            self.if_condition = True
        
    def getVertexShader(self):
        if not self.vertexShader: 
            self.__parserVertexShader()
        return self.vertexShader
        
    def getFragmentShader(self):
        if not self.fragmentShader:
            self.__parserFragmentShader()
        return self.fragmentShader
    
    def resizeNetwork(self, layer = None):
        assert layer
        self.inputWidth = layer.outputWidth
        self.inputHeight = layer.outputHeight
        self.__computeOutputSize()
        
        self.__parserVertexShader()
        self.__parserFragmentShader()
        
    def __parserVertexShader(self):
        self.vertexShader = getShader.getVertexShader(self)
    
    def __parserFragmentShader(self):
        self.fragmentShader = getShader.getFragmentShader(self)
        
    def __computeOutputSize(self):
        if self.inputWidth and self.inputHeight:
            self.outputWidth = (self.inputWidth + 2 * self.padW - self.kW) / self.dW + 1
            self.outputHeight = (self.inputHeight + 2 * self.padH - self.kH) / self.dH + 1
    
    def toJson(self):
        pass
    
if __name__ == '__main__':
    conv = SpatialConvolution(3,44,3,3,2,2)
    conv.inputWidth = 224
    conv.inputHeight = 224
    print conv.padH
        