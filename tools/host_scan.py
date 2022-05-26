from mal_generate import MalGenerator
from mal_generate import config_file, g_config_file, logfile_name
from utils import *

class HostScanGenerator(MalGenerator):
    def __init__(self, config_path, g_config_path) -> None:
        super().__init__(config_path, g_config_path)

    def generate_log(self, size='1480'):
        action = 'allow'
        direction = 'inbound'
        rdirection = 'outbound'

        src = weighted_choice(self.attacker_network)
        dest = weighted_choice(self.victim_networks)
        src_ip = src.gen_random_address()
        dest_ip = dest.gen_random_address()
        protocol = 'icmp'
        
        live_host = randint(0, 100) - 80 # host is not live in 80%

        size = '600'
        logs = [self.log_fmt.format(
            time=get_current_time(), 
            protocol=protocol,
            src_ip=src_ip, src_port=0, 
            dst_ip=dest_ip, dst_port=0, 
            direction=direction, action=action, size=size,
            flags='ICMP Echo Request',
            comment=self.comment)]

        if action == 'allow' and live_host > 0:
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

        return "\n".join(logs)

if __name__ == '__main__':
    hs_gen = HostScanGenerator(config_file, g_config_file)
    hs_gen.setup()
    l = hs_gen.generate_log(size=600)
    hs_gen.launch(logfile_name)
    
