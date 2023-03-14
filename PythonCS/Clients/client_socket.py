import socket as s
import sys

server_address = ('localhost', 5000)
client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        msg = str(input())
        client_socket.send(msg.encode())
        sys.stdout.write(client_socket.recv(1024).decode())
        sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)