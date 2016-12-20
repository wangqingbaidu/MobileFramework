# -*- coding: UTF-8 -*- 
'''
Authorized  by Vlon Jang
Created on 2016年12月16日
Blog: www.wangqingbaidu.cn
Email: wangqingbaidu@gmail.com
From Institute of Computing Technology
©2015-2016 All Rights Reserved.
'''
SIZEOFFLOAT = 4
import ConfigParser, base64, os, json

class NetworkConfig:
    def __init__(self, 
                 cfgfile='kwai_fconv_s2_sig.cfg',
                 weights='kwai_fconv_s2_sig.weights',
                 has_weights = ['convolutional', 'connected'],
                 save_all_weights = False,
                 print_weights = False):
        if not os.path.exists(cfgfile):
            print 'Config file %s can not be read!' % cfgfile
        
        self.cfgfile = cfgfile
        self.weights = weights
        self.has_weights = has_weights
        self.save_all_weights = save_all_weights
        self.print_weights = print_weights
        self.configurations = {}
        self.__parser_network()
        self.__attach_bias_weights()
        
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
                
    def __attach_bias_weights(self):
        file_size = os.path.getsize(self.weights)
        f = open(self.weights)
        head = f.read(4 * SIZEOFFLOAT)
        if self.print_weights:
            print base64.b64encode(head)
        
        layer_num = 1
        total_bytes = 4 * SIZEOFFLOAT
        try:
            #loop layers
            while layer_num < len(self.configurations.keys()):
                if self.configurations[layer_num]['type'].lower() in self.has_weights:
                    bias_num = self.configurations[layer_num]['filters'] * SIZEOFFLOAT
                    former_channels = self.configurations[layer_num - 1]['channels'] \
                        if layer_num == 1 else self.configurations[layer_num - 1]['filters']
                    weights_num = former_channels * bias_num * pow(self.configurations[layer_num]['size'], 2)
                    bias = f.read(bias_num)
                    weights = f.read(weights_num)
                    if self.save_all_weights:
                        self.configurations[layer_num]['bias_all'] = base64.b64encode(bias)
                        self.configurations[layer_num]['weights_all'] = base64.b64encode(weights)
                    
                    self.configurations[layer_num]['bias'] = {}
                    self.configurations[layer_num]['weights'] = {}
                    #loop vec4
                    for l in range(4):
                        bias_from_index = bias_num / 4 * l
                        bias_to_index = bias_num / 4 * (l + 1)
                        weights_from_index = weights_num / 4 * l
                        weights_to_index = weights_num / 4 * (l + 1)
                        self.configurations[layer_num]['bias']['bias_%d' %l] = \
                            base64.b64encode(bias[bias_from_index: bias_to_index])
                        self.configurations[layer_num]['weights']['weights_%d' %l] = \
                            base64.b64encode(weights[weights_from_index: weights_to_index])
                        
                        if self.print_weights:
                            print 'Bias of layer %d part %d\t-->\t' %(layer_num, l), \
                                self.configurations[layer_num]['bias']['bias_%d' %l]
                            print 'Weights of %d part %d\t-->\t' %(layer_num, l), \
                                self.configurations[layer_num]['weights']['weights_%d' %l]
                                
                    total_bytes += bias_num + weights_num
                
                layer_num += 1
        except:
            print 'Error while converting weights, check layer %d\n %s!' %(layer_num, self.configurations[layer_num])
            exit()
        
        assert total_bytes == file_size

if __name__ == '__main__':
    cfg = NetworkConfig(save_all_weights=False, print_weights=True)
#     print json.dumps(cfg.configurations)