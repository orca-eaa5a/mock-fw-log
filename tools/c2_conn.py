import os
from mal_generate import MalGenerator
from mal_generate import config_file, g_config_file, logfile_name
from utils import *

class C2Generator(MalGenerator):
    def __init__(self, config_path, g_config_path) -> None:
        super().__init__(config_path, g_config_path)

    def generate_log(self, size='1480'):
        action = 'allow'
        direction = 'outbound'
        rdirection = 'inbound'

        src = weighted_choice(self.victim_networks)
        dest = weighted_choice(self.c2_servers)
        src_ip = src.gen_random_address()
        src_port = create_os_port()
        dest_ip = dest.ip
        dest_port = dest.port
        protocol = dest.protocol
        
        logs = [self.log_fmt.format(
            time=get_current_time(), 
            protocol=protocol,
            src_ip=src_ip, src_port=src_port, 
            dst_ip=dest_ip, dst_port=dest_port, 
            direction=direction, action=action, size=size,
            flags='S',
            comment=self.comment)]
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

        return "\n".join(logs)

if __name__ == '__main__':
    c2_gen = C2Generator(config_file, g_config_file)
    c2_gen.setup()
    c2_gen.launch(logfile_name)
    
