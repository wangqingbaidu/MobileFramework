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
    """
    Typically each Spatialconvolution layer contains padding, convolution, activation.
    This class firstly use padding parameters to padding X pixels, then do feature extraction and finally activate the output feature map.
    SpatialConvolution layer follow torch7 parameter settings which applies a 2D convolution over an input image composed of several input planes. 
    The input tensor in forward(input) is expected to be a 3D tensor (nInputPlane x height x width).

    Parameters
    ---------------
    @nOutputPlane: The number of output planes the convolution layer will produce.
    @kW: The kernel width of the convolution
    @kH: The kernel height of the convolution
    @dW: The step of the convolution in the width dimension. Default is 1.
    @dH: The step of the convolution in the height dimension. Default is 1.
    @padW: Additional zeros added to the input plane data on both sides of width axis. Default is 0. (kW-1)/2 is often used here.
    @padH: Additional zeros added to the input plane data on both sides of height axis. Default is 0. (kH-1)/2 is often used here.
    @weights: Weights matrix which is based on base64 for visible.
    @bias: Bias matrix which is based on base64 for visible.
    
    Property
    ---------------
    @vertexShader: Spatial convolution in OpenGL vertex shader.
    @fragmentShader: Spatial convolution in OpenGL fragment shader.
    
    Private Methods
    ---------------
    @__parserXXXShader: Parser XXX shader by the layer given parameters and sotre the glsl in xxxShader.
        params: None
        return: None
    @__computeOutputSize: Recompute the size of Output.
        params: None
        return: None
        
    Public Methods
    ---------------
    @resize: Resize the parameters. and recompute the glsl.
        params: iw, ih, ic
            input of width, heights and channels.
        return: None
    @toDic: Convert Module to dict object.
        params: None 
        return: None. 
    """
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
                 activation = None,
                 bias = None,
                 weights = None):
        BaseLayer.__init__(self, nOutputPlane)
        self.kW = kW
        self.kH = kH
        self.dW = dW
        self.dH = dH
        self.padW = padW if padW != None else (kW - 1) / 2
        self.padH = padH if padH != None else (kH - 1) / 2
        self.activation = Activation(activation)
        self.padding = SpatialPadding(self.padW, self.padH)
        
        self.weights = weights
        self.bias = bias
        if nOutputPlane % 4:
            print 'nOutputPlane must be 4*n'
            exit()
        self.group = nOutputPlane / 4
        
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
#         attrib['activation'] = self.activation.toDict()
#         attrib['padding'] = self.padding.toDict()
        return attrib
    
if __name__ == '__main__':
    conv = SpatialConvolution(44,3,3,2,2, activation='leaky')
    conv.inputWidth = 224
    conv.inputHeight = 224
    
    print json.dumps(conv.toDict())
#     print conv.fragmentShader
        