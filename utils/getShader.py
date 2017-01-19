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
"""
This module is used to get shader by the given type of layer.

Methods
-------
@getVertexShader: All layer use the same vertex shader.
    See in GLSL_PATH/vertexShader.glsl

@getFragmentShader: Get fragment shader by the given layer.
    The layer type can be SpatialConvolutional or Activation or SpatialPadding.
    
@getXXXFragmentShader: Get XXX fragment shader.
"""
def getVertexShader(layer = None):
    assert layer
    return open(os.path.join(GLSL_PATH, 'vertexShader.glsl')).read()

def getFragmentShader(layer = None):
    assert layer
    if 'SpatialConvolution' in str(layer.__class__):
        return getSpatialConvolutionalFragmentShader(layer)
    elif 'Activation' in str(layer.__class__):
        return getActivationFragmentShader(layer)
    elif 'SpatialAveragePooling' in str(layer.__class__):
        return getSpatialAveragePoolingFragmentShader(layer)
    elif 'SpatialPadding' in str(layer.__class__):
        return getSpatialPaddingFragmentShader(layer)
    
def getSpatialConvolutionalFragmentShader(layer = None):
    assert layer
#     loop_biases_template = open(os.path.join(GLSL_PATH, 'loop_biases.glsl')).read()
    loop_weights_template = open(os.path.join(GLSL_PATH, 'loop_weights.glsl')).read()
    fragment_template = open(os.path.join(GLSL_PATH, 'fragmentSpatialConvolution.glsl')).read()
    
    loop_weights = ''
    per_width = 1.0 / layer.inputWidth
    per_height = 1.0 / layer.inputHeight
    centerX = layer.kW / 2
    centerY = layer.kH / 2
    fThis = []
    for x in range(layer.kH):
        for y in range(layer.kW):
            fThis.append([(x - centerX) * per_width, (y - centerY) * per_height])
            
    for i in range(layer.kW * layer.kH):
        loop_weights += loop_weights_template.format(kSize = layer.kW * layer.kH, idx = i,
                                                     x_align = fThis[i][0], y_align = fThis[i][1])
            
    return fragment_template.format(weights_num=4*layer.kH*layer.kW,
                                    loop_weights=loop_weights)

def getActivationFragmentShader(layer = None):
    assert layer
    leaky_slope = 0
    if layer.activation == 'leaky':
        leaky_slope = 0.1
    
    return open(os.path.join(GLSL_PATH, 'fragmentActivation.glsl')).read().format(leaky_slope=leaky_slope)

def getSpatialAveragePoolingFragmentShader(layer = None):
    assert layer

def getSpatialPaddingFragmentShader(layer=None):
    assert layer
    return open(os.path.join(GLSL_PATH, 'fragmentSpatialPadding.glsl')).read()    

if __name__ == '__main__':
    print getVertexShader()