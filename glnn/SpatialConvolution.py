# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''

from utils import getShader
from glnn.BaseLayer import BaseLayer
import math, json
from glnn.Activation import Activation
from glnn.SpatialPadding import SpatialPadding
from utils.obj2dict import obj2dict

class SpatialConvolution(BaseLayer):
    __vertexShader = None
    __fragmentShader = None
    
    def __init__(self,
                 nOutputPlane,
                 kW,
                 kH,
                 dW = 1,
                 dH = 1,
                 padW = None,
                 padH = None,
                 activation = None):
        BaseLayer.__init__(self, nOutputPlane)
        self.kW = kW
        self.kH = kH
        self.dW = dW
        self.dH = dH
        self.padW = padW if padW != None else (kW - 1) / 2
        self.padH = padH if padH != None else (kH - 1) / 2
        self.activation = Activation(activation)
        self.padding = SpatialPadding(self.padW, self.padH)
        
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
        self.padding.resize(iw, ih, ic)
        self.inputWidth = self.padding.outputWidth
        self.inputHeight = self.padding.outputHeight
        self.nInputPlane = self.padding.nOutputPlane
        self.__computeOutputSize()
        
        self.activation.resize(self.outputWidth, self.outputHeight, self.nOutputPlane)
        self.__parserVertexShader()
        self.__parserFragmentShader()
        
    def __parserVertexShader(self):
        self.__vertexShader = getShader.getVertexShader(self)
    
    def __parserFragmentShader(self):
        self.__fragmentShader = getShader.getFragmentShader(self)
        
    def __computeOutputSize(self):
        if self.inputWidth and self.inputHeight:
            self.outputWidth = (self.inputWidth + 2 * self.padW - self.kW) / self.dW + 1
            self.outputHeight = (self.inputHeight + 2 * self.padH - self.kH) / self.dH + 1
    
    def toDict(self):
        attrib = obj2dict(self, ['activation', 'padding'])
        attrib['activation'] = self.activation.toDict()
        attrib['padding'] = self.padding.toDict()
        return attrib
    
if __name__ == '__main__':
    conv = SpatialConvolution(43,3,3,2,2, activation='leaky')
    conv.inputWidth = 224
    conv.inputHeight = 224
    
    print json.dumps(conv.toDict())
#     print conv.fragmentShader
        