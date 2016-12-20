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
from scipy.interpolate.interpolate_wrapper import block

GLSL_PATH = '../glsl/'

def getVertexShader(layer = None):
    assert layer
    if 'SpatialConvolution' in str(layer.__class__):
        return getConvolutionalVertexShader()

def getFragmentShader(layer = None):
    assert layer
    if 'SpatialConvolution' in str(layer.__class__):
        return getConvolutionalFragmentShader(layer)

def getConvolutionalVertexShader():
    return open(os.path.join(GLSL_PATH, 'vertexConv.glsl')).read()

def getConvolutionalFragmentShader(layer = None):
    assert layer
    loop_biases_template = open(os.path.join(GLSL_PATH, 'loop_biases.glsl')).read()
    loop_weights_template = open(os.path.join(GLSL_PATH, 'loop_weights.glsl')).read()
    fragment_template = open(os.path.join(GLSL_PATH, 'fragmentShader.glsl')).read()
    
    param = 'out'
    idx = 'weights_idx'
    loop_biases = loop_biases_template.format(param=param, idx=idx)
    weights_params = [param + i for i in ['.r', '.g', '.b', '.a']]
    
    per_width = 1.0 / layer.inputWidth
    per_height = 1.0 / layer.inputHeight
    centerX = layer.kW / 2
    centerY = layer.kH / 2
    fThis = []
    for x in range(layer.kH):
        for y in range(layer.kW):
            fThis.append([(x - centerX) * per_width, (y - centerY) * per_height])
            
    loop_weights = ''
    align = 0
    
    for p in weights_params:
        for i in range(layer.kW * layer.kH):
            loop_weights += loop_weights_template.format(param=p, idx=idx, align=align,
                                                         fThisX = fThis[i][0], fThisY = fThis[i][1])
            align += 1
            
    if_conditions = """
    if (weights_idx * 4 >= biases_num)
    {
        gl_FragColor = vec4(0,0,0,0);
        return;
    }
    """
            
    return fragment_template.format(biases_num=layer.nOutputPlane,
                                    weights_num=layer.nOutputPlane*layer.kH*layer.kW,
                                    if_conditions = if_conditions if layer.if_condition else '',
                                    loop_biases=loop_biases, 
                                    loop_weights=loop_weights,
                                    blockX=layer.blockX,
                                    blockY=layer.blockY,
                                    kW=layer.kW,
                                    kH=layer.kH,
                                    dW=layer.dW,
                                    dH=layer.dH)

if __name__ == '__main__':
    print getConvolutionalVertexShader()