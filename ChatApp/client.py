import socket
import select
import sys
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

def send_msg(sock):
    while True:
        data = sys.stdin.readline()
        sock.send(data.encode())
        sys.stdout.write('<You> ')
        sys.stdout.write(data)
        sys.stdout.flush()

def recv_msg(sock):
    while True:
        data = sock.recv(2048).decode()
        sys.stdout.write(data)

Thread(target=send_msg, args=(server,)).start()
Thread(target=recv_msg, args=(server,)).start()

while True:
    socket_list = [server]
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    
    for sock in read_sockets:
        if sock == server:
            recv_msg(sock)
        else:
            send_msg(sock)

server.close()
