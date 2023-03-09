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

        log = open('Logs/server_four_LOG.txt', 'a')
        log_cache = timestamp + ' ' + str(client_address[0]) + ' ' + str(client_address[1]) + ' ' + str(data)
        log.write(log_cache + '\n')
        log.close()

        if data == 'forcequit':
            client_socket.close()
            break
        if data == 'asklog':
            log = open('Logs/server_four_LOG.txt', 'r')
            log_data = log.read()
            client_socket.send(str.encode(log_data))
            log.close()

        client_socket.send(str.encode(log_cache))
        client_socket.close()

except KeyboardInterrupt:
    print('Server shutting down...')
    sever_socket.close()
    sys.exit(0)
