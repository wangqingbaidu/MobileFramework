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

class SpatialConvolution:
    def __init__(self,
                 nInputPlane = -1,
                 nOutputPlane,
                 kW,
                 kH,
                 dW = 1,
                 dH = 1,
                 padW = 0,
                 padH = 0):
        self.nInputPlane = nInputPlane
        self.nOutputPlane = nOutputPlane
        self.kw = kW
        self.kh = kH
        self.dw = dW
        self.dh = dH
        self.padW = padW if padW else (kW - 1) / 2
        self.padH = padH if padH else (kH - 1) / 2
        self.weights = None
        self.bias = None
    
    def parserVertexShader(self):
        self.vertexShader = getShader.getVertexShader(self)
    
    def toJson(self):
        pass
    
if __name__ == '__main__':
    conv = SpatialConvolution(3,1,3,3)
    conv.parserVertexShader()
    print conv.vertexShader
        