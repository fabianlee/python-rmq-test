#!/usr/bin/env python
#
# Gets local IP address
#
#
import socket

hostname = socket.gethostname()
print(hostname)
ip = socket.gethostbyname(hostname)
print(ip)

