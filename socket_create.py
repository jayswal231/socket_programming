import sys
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Successfully socket connected")
except socket.error as err:
    print("Error %s" %(err))

port = 80

try:
    host_ip = socket.gethostbyname('www.google.com')
except socket.gaierror:
    print("There was error while resolving the host")
    sys.exit()

s.connect((host_ip, port))
print("Successfully connected to the google")