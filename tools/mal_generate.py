import os
import sys
import json
import numpy
from time import sleep

parent_module = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir))
sys.path.append(parent_module)
from generate import Server, Network
from generate import logfile_name, config_file as g_config_file
from utils import *

g_config_file = os.path.join(parent_module, g_config_file)
config_file = 'config'
config_file = os.path.abspath(os.path.join(__file__, os.pardir, config_file))
logfile_name = os.path.abspath(os.path.join(parent_module, logfile_name))

class MalGenerator:
    def __init__(self, config_path, g_config_path) -> None:
        self.g_config_path = g_config_path
        self.config_path = config_path
        self.g_conf = None
        self.conf = None
        self.log_fmt = ''
        self.victim_networks = None
        self.internal_servers = None
        self.c2_servers = None
        self.comment = ''
        self.period = ''
        self.scan_type = ''

        self.conf = self.load_config(self.config_path)
        self.g_conf = self.load_config(self.g_config_path)
        pass
    
    def load_config(self, file_name) -> None:
        _path = file_name
        f = open(_path, 'rt')
        j = ''
        while True:
            l = f.readline()
            if not l:
                break
            if l[0] == "#":
                continue
            j+=l
        j = j.replace("\n", "")

        return json.loads(j)

    def setup(self):
        def setup_network_config(conf):
            nets = []
            weights = []
            if not conf:
                print('network config is empty')
                cider = "/24"
                for r in range(5):
                    ip = gen_random_ip()
                    nets.append(Network(ip+cider))
                    weights.append(1)
                    print('>> [random] setup network config : %s' % (ip+cider))

            else:
                for inet in conf:
                    nets.append(Network(inet['network']))
                    weights.append(inet['weight'])
            net_w = numpy.array(weights)
            net_w = net_w / sum(net_w)
            
            return (nets, net_w)

        def setup_server_config(conf):
            server = []
            weights = []
            server_w = None
            if not conf:
                print('server config is empty')
                for r in range(2):
                    ip = gen_random_ip()
                    pt, prot = gen_wellknown_service_port()
                    server.append(Server(ip, pt, prot))
                    weights.append(1)
                    print('>> [random] setup server config : %s' % (ip+":"+pt))
            else:
                for eserv in conf:
                    protocol = 'tcp'
                    if 'protocol' in eserv:
                        protocol = eserv['protocol']
                    server.append(Server(eserv['ip'], eserv['port'], protocol))
                    weights.append(eserv['weight'])
            
            server_w = numpy.array(weights)
            server_w = server_w / sum(server_w)
            return (server, server_w)
        self.internal_servers = setup_server_config(self.g_conf['internal_servers'])
        self.c2_servers = setup_server_config(self.conf['c2_servers'])

        self.victim_networks = setup_network_config(self.g_conf['internal_network'])
        self.attacker_network = setup_network_config(self.conf['attacker_network'])

        self.log_fmt = self.g_conf['log_fmt']
        self.comment = self.conf['comment']
        
        try:
            if self.conf['period'][-1] == 'm':
                self.period = float(int(self.conf['period'][:-1])*60)
            elif self.conf['period'][-1] == 'h':
                self.period = float(int(self.conf['period'][:-1])*3600)
            elif self.conf['period'][-1] == 's':
                if self.conf['period'][-2] == 'm': #ms
                    self.period = int(self.conf['period'][:-2])*0.1
                else:
                    self.period = float(self.conf['period'][:-1])
        except:
            raise Exception('Invalid Configuration')

        self.scan_type = self.conf['scan_type']
        
    
    def launch(self, logfile_path):
        print('%s launched..' % __file__)
        print('mock log file name is %s' % logfile_path)
        full_path = logfile_path
        f = open(full_path, 'a')
        try:
            while True:
                log = self.generate_log()
                if log:
                    f.write(log+"\n")
                    f.flush()
                    sleep(self.period)
        except KeyboardInterrupt:
            print('interrupt catched..')
            print('log generator stopped')
            f.close()
        pass

    def generate_log(self, size='1480'):
        raise Exception('Not Implemented Error')