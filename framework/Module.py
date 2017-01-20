# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月19日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
import struct

SIZEOFFLOAT = 4
CONFIG_PATH = '../config'

from glnn.SpatialConvolution import SpatialConvolution
from glnn.BaseLayer import BaseLayer
from framework import parsered_frameworks
from utils.getFrameworkAttribute import getFrameworkAttribute
import ConfigParser, base64, os, json

class NetworkConfig:
    """
    This class is used to convert config file and weights to class.
    Only darknet framework is supported now. You can refer to darknet's homepage or github for details.
        http://pjreddie.com/darknet/
        https://github.com/pjreddie/darknet
        
    Parameters
    ---------------
    @cfgfile: darknet-like config file which can be parsered by ConfigParser module.
    @weights: weights file which contains bias and weights corresponds to cfgfile.
    @has_weights: define which type of layer contains weights, It's recommended to leave it be.
    @save_all_weights: default False. By default, it does't save entire weights to weights_all and bias_all attribute.
                       If set to be True, weights_all and bias_all attribute will contains all weights
    @print_weights: default False. Whether print log to console.
    
    Private Methods
    ---------------
    @__parser_network: just use ConfigParser module to convert cfgfile.
        params: None
        return type: dict
    @__attach_bias_weights: attach bias and weights to bias and weights attribute.
        params: None
        return type: None
        ###################################
        This method will check size of weights file and compute the parameters which cfgfile must has. 
        It will raise an error if the two are not equal.
        Bias and weights will split to several parts, which will provide to multi-stage of OpenGL ES.
        The weights file must in size nInputPlane * nOutputPlane * kW * kH and bias is in the front.
        ****************The origin darknet weights perhaps not in this order.****************
    """
    def __init__(self, 
                 cfgfile=os.path.join(CONFIG_PATH,'kwai_fconv_s2_sig.cfg'),
                 weights=os.path.join(CONFIG_PATH,'kwai_fconv_s2_sig.weights'),
                 has_weights = ['convolutional', 'connected'],
                 save_all_weights = False,
                 print_weights = False):
        if not os.path.exists(cfgfile):
            print 'Config file %s can not be read!' % cfgfile
        if not os.path.exists(cfgfile):
            print 'Weights file %s can not be read!' % weights
        
        self.cfgfile = cfgfile
        self.weights = weights
        self.has_weights = has_weights
        self.save_all_weights = save_all_weights
        self.print_weights = print_weights
        self.configurations = {}
        self.__parser_network()
        self.__attach_biases_weights()
        
    def __parser_network(self):
        cf = ConfigParser.ConfigParser()
        cf.read(self.cfgfile)      
        
        for sec in cf.sections():
            self.configurations[int(sec)] = {}
            for k, v in cf.items(sec):
                try:
                    self.configurations[int(sec)][k] = int(v)
                except:
                    self.configurations[int(sec)][k] = v
                
    def __attach_biases_weights(self):
        file_size = os.path.getsize(self.weights)
        f = open(self.weights)
        head = f.read(4 * SIZEOFFLOAT)
        if self.print_weights:
            print base64.b64encode(head)
        
        #Network configuration starts from 1
        layer_num = 1
        total_bytes = 4 * SIZEOFFLOAT
        try:
            #loop layers
            for layer_num in range(1, len(self.configurations.keys())):
                if self.configurations[layer_num]['type'].lower() in self.has_weights:
                    #Total number of weights in this layer.
                    former_channels = self.configurations[layer_num - 1]['channels'] \
                        if layer_num == 1 else self.configurations[layer_num - 1]['filters']
                    this_channels = self.configurations[layer_num]['filters']
                    bias_num = this_channels * SIZEOFFLOAT
                    weights_num =  this_channels * pow(self.configurations[layer_num]['size'], 2) * former_channels * SIZEOFFLOAT
                    bias = f.read(bias_num)
                    weights = f.read(weights_num)
                    #------------------------------------- Append bias & weights----------------------------#
                    #Append float zero byte stream
                    z = struct.pack('f', 0.0)
                    append_num = (4 - this_channels % 4) % 4
                    bias += z * append_num
                    weights += z * append_num * pow(self.configurations[layer_num]['size'], 2) * former_channels
                    
                    #Convert to time of 4.
                    this_channels += append_num
                    self.configurations[layer_num]['filters'] = this_channels
                    
                    #------------------------------------- Get average bias ----------------------------#
                    #Compute parts
                    this_parts = this_channels / 4
                    former_parts = int(round(former_channels / 4.0))
                                          
                    #Get float value of each bias
                    bias_float = [v / former_parts for v in struct.unpack('f' * this_channels, bias)]
                    bias = struct.pack('f' * this_channels, *bias_float)                                   
                    
                    #------------------------------------- Attaching weights ----------------------------#
                    if self.save_all_weights:
                        self.configurations[layer_num]['bias_all'] = base64.b64encode(bias)
                        self.configurations[layer_num]['weights_all'] = base64.b64encode(weights)
                    
                    self.configurations[layer_num]['bias'] = {}
                    self.configurations[layer_num]['weights'] = {}
                    
                    #loop biases vec4, change bias part when featureMapOut part changes.
                    for l in range(this_parts):
                        #Get index of each bias part
                        bias_from_index = bias_num / this_parts * l
                        bias_to_index = bias_num / this_parts * (l + 1)
                        self.configurations[layer_num]['bias'][l] = \
                            base64.b64encode(bias[bias_from_index: bias_to_index])
                            
                        if self.print_weights:
                            print 'Bias of layer %d part %d\t-->\t' %(layer_num, l), \
                                self.configurations[layer_num]['bias'][l]
                    
                    #Separate weights to this_parts * former_parts, each of which will compute once.
                    weights_num_per_parts = weights_num / this_parts / former_parts            
                    for t in range(this_parts):
                        self.configurations[layer_num]['weights'][t] = {}
                        #loop weights vec4
                        for l in range(former_parts):
                            weights_from_index = weights_num_per_parts * (l + t * former_parts)
                            weights_to_index = weights_num_per_parts * (l + t * former_parts + 1)
                            self.configurations[layer_num]['weights'][t][l] = \
                                base64.b64encode(weights[weights_from_index: weights_to_index])
                            
                            if self.print_weights:
                                print 'Weights of %d part %d\t-->\t' %(layer_num, l), \
                                    self.configurations[layer_num]['weights'][t][l]
                                
                    total_bytes += bias_num + weights_num
        except Exception, e:
            print e
            print 'Error while converting weights, check layer %d\n%s!' %(layer_num, self.configurations[layer_num])
            raise e
        
        assert total_bytes == file_size

class Module:
    """
    This class is act like Module in torch, the `container` attribute is set to contain all layer in the model.
        
    Parameters
    ---------------
    @w: image width.
    @h: image height.
    @c: image channel, default 3, must be 1 or 3.
    @config: NetworkConfig instance. 
             If this parameter is set, @w, @h, @c will be ignored, and will call resizeNetwork automaticly.
    
    Private Methods
    ---------------
    @__init_from_config: use a NetworkConfig instance to init Module.
        params: NetworkConfig instance
        return: None
        ###################################
        Initial from config contains two phase.
        In phase one. Network input_width and input_height, and input_channels will be set.
        In phase two. Use getFrameworkAttribute to get attribute name by the given framework.
                      Then init layer by layer. 
                      Now only SpatialConvolutional with padding and stride supported.
    
    Public Methods
    --------------    
    @setWidthHeight: Set attributes of network
        params: w, h, c which is width, height, channels of input image.
        reutrn: None
        
    @add: Add layers which based on BaseLayer otherwise will not be parsered.
        params: Layer instance
        return: None.
        
    @resizeNetwork: Compute the following layers width and height
        params: None 
        return: None
        
    @toJson: Convert Module to json object.
        params: None 
        return: Json string of model in glsl. 
    """
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
            
    def __init_from_config(self, config = None):
        assert type(config) == dict
        framework = 'darknet'
        ################################PHASE ONE. Get network configurations.################################
        try:
            assert config[0]['type'] == 'net' and config[0]['framework'] in parsered_frameworks
            framework = config[0]['framework']
            self.inputWidth = config[0]['width']
            self.inputHeight = config[0]['height']
            self.inputChannels = config[0]['channels']
        except Exception,e:
            print e, 'Check network configurations.'
            exit()
        
        ################################PHASE TWO. Get layers configurations.################################
        l = 1
        self.container = []
        try:
            while l < len(config.keys()):
                if config[l]['type'].lower() == 'convolutional':
                    self.container.append(SpatialConvolution(config[l][getFrameworkAttribute('nOutputPlane', framework)],
                                                             config[l][getFrameworkAttribute('kW', framework)],
                                                             config[l][getFrameworkAttribute('kH', framework)],
                                                             config[l][getFrameworkAttribute('dW', framework)],
                                                             config[l][getFrameworkAttribute('dH', framework)],
                                                             config[l][getFrameworkAttribute('activation', framework)],
                                                             config[l][getFrameworkAttribute('bias', framework)],
                                                             config[l][getFrameworkAttribute('weights', framework)]))
                l += 1
        except Exception,e:
            print e
            exit()
        
        self.resizeNetwork()
                
    def setWidthHeight(self, w = None, h = None, c = None):
        try:
            self.inputWidth = int(w)
            self.inputHeight = int(h)
            self.inputChannels = int(c) 
        except:
            print 'Error settings of width or height or channels', w, h, c
            exit()
        
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
    
  
if __name__ == '__main__':
    cfg = NetworkConfig(save_all_weights=False, print_weights=False)
    model = Module(config = cfg.configurations)
#     model.add(SpatialConvolution(3,3,3, activation='relu'))
#     model.add(SpatialConvolution(44,3,3, activation='leaky'))
#     model.resizeNetwork()
    print model.toJson()