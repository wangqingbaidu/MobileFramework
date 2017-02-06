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
from utils.obj2dict import obj2dict

class SpatialConvolution(BaseLayer):
    """
    Typically each Spatialconvolution layer contains padding, convolution, activation.
    Padding size is ignored, padding model same will be used.
    SpatialConvolution layer follow torch7 parameter settings which applies a 2D convolution over an input image. 
    The input tensor in forward(input) is expected to be a 3D tensor (nInputPlane x height x width).

    Parameters
    ---------------
    @nOutputPlane: The number of output planes the convolution layer will produce.
    @kW: The kernel width of the convolution
    @kH: The kernel height of the convolution
    @dW: The step of the convolution in the width dimension. Default is 1.
    @dH: The step of the convolution in the height dimension. Default is 1.
    @weights: Weights matrix which is based on base64 for visible.
    @bias: Bias matrix which is based on base64 for visible.
    @first: First layer of this model. Default is False. If Ture, this layer can't be decoded.
    
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
                 activation = None,
                 bias = None,
                 weights = None,
                 first = False):
        BaseLayer.__init__(self, nOutputPlane)
        self.kW = kW
        self.kH = kH
        self.dW = dW
        self.dH = dH
        self.first = first
        assert activation.lower() in ['relu', 'leaky']
        self.leaky_slope = 0.0 if activation.lower() == 'relu' else 0.0001
        get_activation = lambda t: "activation = clamp(step(0.0, tmp + feature_map_out), 0.0, 1.0);" if t == 'relu' else \
            "activation = clamp(step(0.0, tmp + feature_map_out) + vec4(0.0001), 0.0, 1.0);" 
        self.activation = get_activation(activation.lower())
        
        self.weights = weights
        self.bias = bias
#         if nOutputPlane % 4:
#             print 'nOutputPlane must be 4*n'
#             exit()
        self.parts = nOutputPlane / 4 + (1 if nOutputPlane % 4 else 0)
        
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
        self.inputWidth = iw
        self.inputHeight = ih
        self.nInputPlane = ic
        self.__computeOutputSize()
        self.__parserVertexShader()
        self.__parserFragmentShader()
        
    def __parserVertexShader(self):
        self.__vertexShader = getShader.getVertexShader(self)
    
    def __parserFragmentShader(self):
        self.__fragmentShader = getShader.getFragmentShader(self)
        
    def __computeOutputSize(self):
        if self.inputWidth and self.inputHeight:
            self.outputWidth = (self.inputWidth - 1) / self.dW + 1
            self.outputHeight = (self.inputHeight - 1) / self.dH + 1
    
    def toDict(self):
        attrib = obj2dict(self, [])
        return attrib
    
if __name__ == '__main__':
    conv = SpatialConvolution(44,3,3,2,2, activation='leaky')
    conv.inputWidth = 224
    conv.inputHeight = 224
    
    print json.dumps(conv.toDict())
#     print conv.fragmentShader
        