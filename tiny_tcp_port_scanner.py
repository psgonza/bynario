#!/usr/bin/env python

""" 
  Simple-simple-simple TPC port scanner using sockets
  
  Example:
  $> python tiny_tcp_port_scanner.py

  1) Enter host or ip to scan: 192.168.1.1
  2) Enter first port: 1
  3) Enter last port: 1024

  * Starting scan on 192.168.1.1 ports 1-1024
  (TCP) Port 22: OPEN
  (TCP) Port 111: OPEN

  * Finished scan on 192.168.1.1 ports 1-1024

"""
#!/usr/bin/env python
from socket import *
import signal
from sys import exit

s_timeout=0.2
target = raw_input('1) Enter host or ip to scan: ')

def signal_handler(signal, frame):
    print('\n* Ctrl+C captured... Exiting')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
    
try:
    initial = int(raw_input('2) Enter first port: '))
    final = int(raw_input('3) Enter last port: '))
except ValueError:
    print("\n-E- Please enter an integer as first/last port\n")
    exit()

try:
    targetIP = gethostbyname(target)
except:
    print('\n-E- {0} is not a valid IP address\n'.format(target))
    exit()

print('\n* Starting scan on {0} ports {1}-{2}\n'.format(targetIP,initial,final))

for i in range(initial,final):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(s_timeout)
    result = s.connect_ex((targetIP, i))
    if(result == 0) :
        print('(TCP) Port {0}: OPEN'.format(i))
    s.close()

print('\n* Finished scan on {0} ports {1}-{2}\n'.format(targetIP,initial,final))

