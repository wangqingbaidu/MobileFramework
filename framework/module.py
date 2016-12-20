# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
from glnn.SpatialConvolution import SpatialConvolution
from glnn.BaseLayer import BaseLayer

class Module:
    def __init__(self, config = None):
        self.container = []
        if config:
            self.__init_from_config(config)
        
    def add(self, layer = None):
        if BaseLayer in layer.__class__.__bases__:
            if len(self.container) > 0:
                layer.nInputPlane = self.container[-1].nOutputPlane
            self.container.append(layer)
            
    def toJson(self):
        pass
    
    def __init_from_config(self, config = None):
        assert config
        pass
    
if __name__ == '__main__':
    model = Module()
    model.add(SpatialConvolution(3,3,3,3))
    print model.container[0].vertexShader