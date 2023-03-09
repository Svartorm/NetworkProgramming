from socket import *

server_address = ('localhost', 5000)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(server_address)

strsend = 'Hello, world!'
client_socket.send(str.encode(strsend))
client_socket.close()