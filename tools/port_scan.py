from mal_generate import MalGenerator
from mal_generate import config_file, g_config_file, logfile_name
from utils import *
from time import sleep

class PortScanGenerator(MalGenerator):
    port_scan_cnt=1
    def __init__(self, config_path, g_config_path) -> None:
        super().__init__(config_path, g_config_path)

    def launch(self, logfile_path):
        print('%s launched..' % __file__)
        print('mock log file name is %s' % logfile_path)
        full_path = logfile_path
        f = open(full_path, 'a')
        try:
            src = weighted_choice(self.victim_networks)
            dest = weighted_choice(self.internal_servers)
            while True:
                log = self.generate_log(src, dest)
                if log:
                    f.write(log+"\n")
                    f.flush()
                    PortScanGenerator.port_scan_cnt+=1
                    sleep(self.period)
                if PortScanGenerator.port_scan_cnt > 65535:
                    break
        except KeyboardInterrupt:
            print('interrupt catched..')
            print('log generator stopped')
            f.close()
        
        print('log generator stopped')
        f.close()
        pass

    def generate_log(self, src, dest, size='1480'):
        action = 'deny'
        direction = 'inbound'
        rdirection = 'outbound'

        src_ip = src.gen_random_address()
        src_port = create_os_port()

        dest_ip = dest.ip
        dest_port = PortScanGenerator.port_scan_cnt
        serv_protocol = dest.protocol

        if 'tcp' in self.scan_type:
            protocol = 'tcp'
        else:
            protocol = 'udp'
        
        if protocol == 'tcp':
            logs = [self.log_fmt.format(
            time=get_current_time(), 
            protocol=protocol,
            src_ip=src_ip, src_port=src_port, 
            dst_ip=dest_ip, dst_port=dest_port, 
            direction=direction, action=action, size=size,
            flags='S',
            comment=self.comment)]
            if PortScanGenerator.port_scan_cnt == dest.port:
                action = 'allow'
                
            if action == 'allow':
                if serv_protocol == protocol:
                    if PortScanGenerator.port_scan_cnt == dest.port:
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
                        if self.scan_type == 'tcp_open':
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
                        # elif self.scan_type == 'tcp_syn':
                            

                    else :
                        logs.append(
                            self.log_fmt.format(
                            time=get_current_time(), 
                            protocol=protocol,
                            dst_ip=src_ip, dst_port=src_port, 
                            src_ip=dest_ip, src_port=dest_port, 
                            direction=rdirection, action=action, size='40',
                            flags='RA',
                            comment=self.comment)
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

if __name__ == '__main__':
    hs_gen = PortScanGenerator(config_file, g_config_file)
    hs_gen.setup()
    hs_gen.launch(logfile_name)
    
