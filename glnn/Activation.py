# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月20日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
from glnn.BaseLayer import BaseLayer
from glsl import getShader
class Activation(BaseLayer):
    __vertexShader = None
    __fragmentShader = None
    
    def __init__(self,
                 activation):
        assert activation.lower() in ['relu', 'leaky']
        self.activation = activation.lower()
        
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
        self.outputWidth = self.inputWidth = iw
        self.outputHeight = self.inputHeight = ih
        self.nOutputPlane = self.nInputPlane = ic
        
        self.__parserVertexShader()
        self.__parserFragmentShader()
        
    def __parserVertexShader(self):
        self.__vertexShader = getShader.getVertexShader(self)
    
    def __parserFragmentShader(self):
        self.__fragmentShader = getShader.getFragmentShader(self)
        
    
    def toJson(self):
        pass
        
        
if __name__ == '__main__':
    a = Activation()
    print a.fragmentShader