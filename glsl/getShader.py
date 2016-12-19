# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
import os

GLSL_PATH = '../glsl/'

def getVertexShader(layer = None):
    assert layer
    if 'SpatialConvolution' in str(layer.__class__):
        return getConvolutionalVertexShader()

def getConvolutionalVertexShader():
    return open(os.path.join(GLSL_PATH, 'vertexConv.glsl')).read()

if __name__ == '__main__':
    print getConvolutionalVertexShader()