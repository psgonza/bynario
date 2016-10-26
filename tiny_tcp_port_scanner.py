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

from socket import *
import sys

target = raw_input('1) Enter host or ip to scan: ')
try:
    initial = int(raw_input('2) Enter first port: '))
    final = int(raw_input('3) Enter last port: '))
except ValueError:
    print("\n-E- Please enter an integer as first/last port")
    sys.exit()

try:
    targetIP = gethostbyname(target)
except:
    print('\n-E- {} is not a valid IP address'.format(target))
    sys.exit()

print('\n* Starting scan on {} ports {}-{}'.format(targetIP,initial,final))

for i in range(initial,final):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.2)
    result = s.connect_ex((targetIP, i))
    if(result == 0) :
        print('(TCP) Port {}: OPEN'.format(i))
    s.close()

print('\n* Finished scan on {} ports {}-{}'.format(targetIP,initial,final))
