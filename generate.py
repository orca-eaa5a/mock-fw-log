import os
import sys
from copy import deepcopy
import json
from random import randint
from time import sleep
import numpy
from utils import *

py_version = str(sys.version_info.major)+"."+str(sys.version_info.minor)
config_file = 'config'
logfile_name = 'noise.txt'

class Network:
    def __init__(self, networkAddrss) -> None:
        self.networkCider = ''
        self.networkAddr = ''
        self.hostRange = None
        self.delta = []
        self.parse_addr(networkAddrss)
        self.def_host_range()
        pass

    def parse_addr(self, networkAddress) -> None:
        if "/" in networkAddress:
            self.networkAddr, self.networkCider = networkAddress.split('/')

        else:
            self.networkCider = ''
            self.networkAddr = networkAddress # <-- this is hostAddress
            
        pass

    def gen_random_address(self) -> str:
        ip, _ = deepcopy(self.hostRange)
        idx = 0
        for d in self.delta:
            o = randint(0, d)
            ip[idx] += o
            idx+=1

        return ".".join(map(str, ip))
    
    def def_host_range(self) -> None:
        if not self.networkCider:
            self.hostRange = (self.networkAddr, self.networkAddr)
        else:
            remain = 32 - int(self.networkCider)
            binAddr = ''
            for n in self.networkAddr.split("."):
                b = format(int(n), "b")
                if len(b) != 8:
                    b = ("0"*(8-len(b)) + b)
                binAddr += b
                
            networkAddr = binAddr[:int(self.networkCider)] + "0"*remain
            
            _networkAddr = []
            idx = 0
            while 4 > idx:
                if int(len(networkAddr)/8) != 0:
                    _networkAddr.append(int(networkAddr[:8], 2))
                    networkAddr = networkAddr[8:]
                    idx+=1
                else:
                    remain = 8 - len(networkAddr)
                    _networkAddr.append(int(networkAddr + "0"*remain, 2))
                    idx+=1

            networkAddr = binAddr[:int(self.networkCider)] + "1"*remain
            _networkAddr_l = []
            idx = 0
            while 4 > idx:
                _networkAddr_l.append((int(networkAddr[:8], 2)))
                networkAddr = networkAddr[8:]
                idx+=1
            
            self.hostRange = (_networkAddr, _networkAddr_l)
            for n, h in zip(_networkAddr, _networkAddr_l):
                self.delta.append(h-n)
        pass    
    
class Server:
    def __init__(self, ip:str, port:str, protocol='tcp') -> None:
        self.ip = ip
        self.port = port
        self.protocol = protocol
        pass

class Generator:
    def __init__(self, config_path, logfile_name) -> None:
        self.config_file = config_path
        self.config = None
        self.log_fmt = ''
        self.internal_networks = None
        self.external_networks = None
        self.internal_servers = None
        self.external_servers = None
        self.deny_weight = None
        self.direction_weights = None
        self.protocols = None
        self.comment = ''
        self.period = 0
        self.load_config()
        self.logfile_name = logfile_name
        pass
    
    def load_config(self) -> None:
        _path = os.path.join(os.path.curdir, self.config_file)
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
        self.config = json.loads(j)

        pass

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
                for r in range(5):
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

        def setup_protocol_config(conf):
            prt = []
            weights = []
            for p in conf:
                prt.append(p['name'])
                weights.append(p['weight'])
            prt_w = numpy.array(weights)
            prt_w = prt_w / sum(prt_w)

            return (prt, prt_w)

        def setup_direction_config(conf):
            keys = list(conf.keys())
            weights = [conf[keys[0]], conf[keys[1]]]
            dir_w = numpy.array(weights)
            dir_w = dir_w / sum(dir_w)

            return (keys, dir_w)

        def setup_rate_config(conf):
            deny_rate = conf
            return (["allow", "deny"], [1-(float(deny_rate)/100), float(deny_rate)/100])

        self.internal_networks = setup_network_config(conf=self.config['internal_network'])
        self.external_networks = setup_network_config(conf=self.config['external_network'])

        self.internal_servers = setup_server_config(conf=self.config['internal_servers'])
        self.external_servers = setup_server_config(conf=self.config['external_servers'])

        self.protocols = setup_protocol_config(conf=self.config['protocols'])
        self.direction_weights = setup_direction_config(self.config['direction_weight'])
        self.deny_weight = setup_rate_config(self.config['deny_rate'])
        self.log_fmt = self.config['log_fmt']
        self.comment = self.config['comment']
        self.period = self.config['period']

    def launch(self):
        print('mock fw log daemon launched..')
        print('mock log file name is %s' % self.logfile_name)
        full_path = os.path.join(os.path.curdir, self.logfile_name)
        f = open(full_path, 'a')
        try:
            while True:
                log = self.generate_log()
                if log:
                    f.write(log+"\n")
                    f.flush()
                    sleep(self.period*0.3)
        except KeyboardInterrupt:
            print('interrupt catched..')
            print('log generator stopped')
            f.close()
        pass


    def log_factory(self, protocol, src_ip, src_port, dest_ip, dest_port, serv_protocol, direction, action, size='1480'):
        rdirection = ''
        if direction == 'inbound':
            rdirection = 'outbound'
        else:
            rdirection = 'inbound'
        if protocol != 'icmp' and serv_protocol != protocol and direction == 'outbound':
            return ''

        if protocol == 'tcp':
            logs = [self.log_fmt.format(
            time=get_current_time(), 
            protocol=protocol,
            src_ip=src_ip, src_port=src_port, 
            dst_ip=dest_ip, dst_port=dest_port, 
            direction=direction, action=action, size=size,
            flags='S',
            comment=self.comment)]
            if action == 'allow' and serv_protocol == protocol:
                logs.append(
                    self.log_fmt.format(
                        time=get_current_time(), 
                        protocol=protocol,
                        dst_ip=src_ip, dst_port=src_port, 
                        src_ip=dest_ip, src_port=dest_port, 
                        direction=rdirection, action=action, size=size,
                        flags='SA',
                        comment=self.comment)
                )
                logs.append(
                    self.log_fmt.format(
                        time=get_current_time(), 
                        protocol=protocol,
                        src_ip=src_ip, src_port=src_port, 
                        dst_ip=dest_ip, dst_port=dest_port, 
                        direction=direction, action=action, size=size,
                        flags='FA',
                        comment=self.comment)
                )
        elif protocol == 'icmp':
            size = '600'
            logs = [self.log_fmt.format(
                time=get_current_time(), 
                protocol='icmp',
                src_ip=src_ip, src_port=0, 
                dst_ip=dest_ip, dst_port=0, 
                direction=direction, action=action, size=size,
                flags='ICMP Echo Request',
                comment=self.comment)]

            if action == 'allow':
                logs.append(
                    self.log_fmt.format(
                        time=get_current_time(), 
                        protocol='icmp',
                        dst_ip=src_ip, src_port=0, 
                        src_ip=dest_ip, dst_port=0, 
                        direction=rdirection, action=action, size=size,
                        flags='ICMP Echo Response',
                        comment=self.comment
                    )
                )

        elif protocol == 'udp':
            if protocol != serv_protocol:
                action = 'deny'
            logs = [self.log_fmt.format(
                time=get_current_time(), 
                protocol='udp',
                src_ip=src_ip, src_port=src_port, 
                dst_ip=dest_ip, dst_port=dest_port, 
                direction=direction, action=action, size=size,
                flags='',
                comment=self.comment)]

        return "\n".join(logs)

    

    def generate_log(self):
        protocol = weighted_choice(self.protocols)
        action = weighted_choice(self.deny_weight)
        direction = weighted_choice(self.direction_weights)
        serv_protocol = 'tcp'

        if direction == 'inbound':
            src = weighted_choice(self.external_networks)
            dest = weighted_choice(self.internal_servers)
            src_ip = src.gen_random_address()
            src_port = create_os_port()

            dest_ip = dest.ip
            dest_port = dest.port
            serv_protocol = dest.protocol

        else:
            src = weighted_choice(self.internal_networks)
            dest = weighted_choice(self.external_servers)

            dest_ip = dest.ip
            dest_port = dest.port
            serv_protocol = dest.protocol

            src_ip = src.gen_random_address()
            src_port = create_os_port()
            
        
        _log = self.log_factory(protocol, src_ip, src_port, dest_ip, dest_port, serv_protocol, direction, action)

        return _log


if __name__ == '__main__':
    g = Generator(config_path=config_file, logfile_name=logfile_name)
    g.setup()
    g.launch()