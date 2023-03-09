from socket import *

server_address = ('localhost', 5000)

sever_socket = socket(AF_INET, SOCK_STREAM)
sever_socket.bind(server_address)
sever_socket.listen(1)
client_socket, client_address = sever_socket.accept()
data = client_socket.recv(1024)
print(str(data, 'utf-8'))

client_socket.close()
sever_socket.close()