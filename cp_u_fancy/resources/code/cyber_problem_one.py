import sys
import os
import socket
import subprocess

import multiprocessing as mp

## Fix with inheritence and base class later!!!
class PortScanner:
    def __init__(self, ip: str, ports: list = [], timing: int = 3, scan_type: str = "TCP SYN"):
        self.ip = ip
        self.ports = ports if len(ports) else [i for i in range(1, 65536)]
        self.timing = timing
        self.open_ports = []
        
        def probe(self, port: int):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                r = sock.connect_ex((self.ip, port))
                
                if r == 0:
                    result = r
                socket.close()
            except:
                pass
                
            return port if result == 0 else False
            
        # Fix
        def execute(self):
            with mp.Pool(os.cpu.count()) as pool:
                processes = [pool.apply_async(self.probe, args=(port,)) for port in self.ports]
                results = list(filter(lambda x: x != False, [p.get() for p in processes]))
                
                return results
               
class PortScannerNmap:
    def __init__(self, ip: str, ports: list = [], timing: int = 3, scan_type: str = "TCP SYN"):
        self.ip = ip
        self.ports = ports if len(ports) else [i for i in range(1, 65536)]
        self.timing = timing
        self.open_ports = []
        
    def run(self, cmd: list):
        ret = subprocess.run(cmd, capture_output=True, timeout=5)
        return ret.stdout.decode().strip().split('\n')
        
    def execute(self):
        results = self.run(['sudo', 'nmap', '-T3', '-sS', self.ip])
        print(results)
        portscan = list(filter(lambda x: 'tcp' in x or 'udp' in x, results))
        return f'Portscan found {len(portscan)} ports on {self.ip}'
        
nmap = PortScannerNmap('192.168.56.102')

print(nmap.execute())
