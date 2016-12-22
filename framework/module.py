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
import json
from distutils.command.config import config

class Module:
    inputWidth = None
    inputHeight = None
    def __init__(self, 
                 w = None,
                 h = None,
                 c = 3,
                 config = None):
        self.container = []
        
        if config:
            self.__init_from_config(config)
        else:
            self.setWidthHeight(w, h, c)
            
    def setWidthHeight(self, w = None, h = None, c = None):
        try:
            self.inputWidth = int(w)
            self.inputHeight = int(h)
            self.inputChannels = int(c) 
        except:
            print 'Error settings of width or height or channels', w, h, c
        
    def add(self, layer = None):
        if BaseLayer in layer.__class__.__bases__:
            if len(self.container) > 0:
                layer.nInputPlane = self.container[-1].nOutputPlane
            self.container.append(layer)
            
    def resizeNetwork(self):
        assert self.inputWidth and self.inputHeight and self.inputChannels
        for i in range(len(self.container)):
            if i:
                self.container[i].resize(self.container[i - 1].outputWidth, self.container[i - 1].outputHeight,\
                                         self.container[i - 1].nOutputPlane)
            else:
                self.container[i].resize(self.inputWidth, self.inputHeight, self.inputChannels)
        
        
    def toJson(self):
        return json.dumps([l.toDict() for l in self.container])
    
    def __init_from_config(self, config = None):
        assert type(config) == dict
        ################PHASE ONE. Get network configurations.################
        try:
            assert config[0]['type'] == 'net'
            self.w = config[0]['width']
            self.h = config[0]['height']
            self.c = config[0]['channels']
        except Exception,e:
            print e, 'Check network configurations.'
            exit()
        
        ################PHASE TWO. Get layers configurations.################
        l = 1
        try:
            while l < len(config.keys()):
                pass
        except:
            pass
        
    
if __name__ == '__main__':
    model = Module(224,224,3)
    model.add(SpatialConvolution(3,3,3, activation='relu'))
    model.add(SpatialConvolution(44,3,3, activation='leaky'))
    model.resizeNetwork()
    print model.toJson()