import os
import sys
import json
import numpy

parent_module = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir))
sys.path.append(parent_module)
from generate import Server, Network
from generate import logfile_name, config_file as g_config_file
from utils import *

config_file = 'config'

class MalGenerator:
    def __init__(self, config_path, g_config_path, logfile_name) -> None:
        self.g_config_path = g_config_path
        self.config_file = config_path
        self.g_conf = None
        self.conf = None
        self.log_fmt = ''
        self.victim_networks = None
        self.internal_servers = None
        self.c2_servers = None
        self.comment = ''
        self.period = ''

        self.conf = self.load_config(self.config_path)
        self.g_conf = self.load_config(self.g_config_path)

        self.logfile_name = logfile_name
        pass
    
    def load_config(self, file_name) -> None:
        _path = os.path.join(os.path.curdir, file_name)
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
        self.period = self.conf['period']