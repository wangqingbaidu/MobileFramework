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
                 has_weights = ['convolutional', 'connected']):
        if not os.path.exists(cfgfile):
            print 'Config file %s can not be read!' % cfgfile
        
        self.cfgfile = cfgfile
        self.weights = weights
        self.has_weights = has_weights
        self.configurations = {}
        self.__parser_network()
        self.__attach_bias_weights()
        
    def __parser_network(self):
        cf = ConfigParser.ConfigParser()
        cf.read(self.cfgfile)      
        
        for sec in cf.sections():
            self.configurations[int(sec)] = {}
            for k, v in cf.items(sec):
                self.configurations[int(sec)][k] = v
                
    def __attach_bias_weights(self):
        file_size = os.path.getsize(self.weights)
        f = open(self.weights)
        head = f.read(4 * SIZEOFFLOAT)
        print base64.b64encode(head)
        
        layer_num = 1
        total_bytes = 4 * SIZEOFFLOAT
        try:
            while layer_num < len(self.configurations.keys()):
                if self.configurations[layer_num]['type'].lower() in self.has_weights:
                    bias_num = int(self.configurations[layer_num]['filters']) * SIZEOFFLOAT
                    former_channels = self.configurations[layer_num - 1]['channels'] \
                        if layer_num == 1 else self.configurations[layer_num - 1]['filters']
                    weights_num = int(former_channels) * bias_num * pow(int(self.configurations[layer_num]['size']), 2)
                    
                    self.configurations[layer_num]['bias'] = base64.b64encode(f.read(bias_num))
                    self.configurations[layer_num]['weights'] = base64.b64encode(f.read(weights_num))
                    total_bytes += bias_num + weights_num
                
                layer_num += 1
        except:
            print 'Error while converting weights, check layer %d\n %s!' %(layer_num, self.configurations[layer_num])
            exit()
        
        assert total_bytes == file_size

if __name__ == '__main__':
    cfg = NetworkConfig()
    print json.dumps(cfg.configurations)