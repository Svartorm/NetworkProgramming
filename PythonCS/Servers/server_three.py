from socket import *
import sys
import time

server_address = ('localhost', 5000)
sever_socket = socket(AF_INET, SOCK_STREAM)
sever_socket.bind(server_address)
sever_socket.listen(1)

try:
    while True:
        client_socket, client_address = sever_socket.accept()
        print('Connection from', client_address, 'to', server_address, 'established.')

        data = client_socket.recv(1024).decode()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(timestamp, str(data))

        f = open('Logs/server_three_LOG.txt', 'a')
        f.write(timestamp + ' ' + str(client_address[0]) + ' ' + str(client_address[1]) + ' ' + str(data) + '\n')
        f.close()

        client_socket.close()

except KeyboardInterrupt:
    print('Server shutting down...')
    sever_socket.close()
    sys.exit(0)
