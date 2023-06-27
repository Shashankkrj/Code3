import socket
import sys
try:
    sock = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM) #socket family is the address family of IPV4 #type of socket for TCP is SOCK_STREAM  type of socket for UDP is SOCK_DGRAM
except socket.error as err:
    print("Failed to create a socket")
    print("Reason: "+str(err))
    sys.exit()
print('socket created')

target_host = input("Enter the target_host name to connect: ")
target_port = input("Enter the target port: ")
try:
    sock.connect((target_host, int(target_port)))
    print("socket connected to: "+target_host+" on port: "+target_port)
    sock.shutdown(2)
except socket.error as err:
    print("Failed to create a socket")
    print("Reason"+str(err))
    sys.exit()
