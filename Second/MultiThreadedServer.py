import socket
from _thread import *

server_socket = socket.socket()

host = '127.0.0.1'
port = 12345
ThreadCount = 0  # Tracks the no. of threads running

try:
    server_socket.bind((host,port))
except socket.error as e:
    print(str(e))
print("Server: Waiting for connection...")
server_socket.listen(5)

def client_thread(connection):
    connection.send(str.encode("Server: Welcome to the server"))
    while True:
        data = connection.recv(1024)
        reply = "Server: "+ data.decode("utf-8")
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, addr = server_socket.accept()
    print("Server: Connected to "+ addr[0] + str(addr[1]))
    start_new_thread(client_thread, (client,))
    ThreadCount += 1
    print("Server: ThreadNumber "+ str(ThreadCount))

server_socket.close()