from socket import *
import sys
import time

server_ip = 'localhost'
server_port = 0

print('Client starting...')

def setServer():
    global server_ip
    server_ip = input('Enter server IP: ')
    global server_port
    server_port = int(input('Enter server port: '))
setServer()

try:
    while True:
        server_address = (server_ip, server_port)
        client_socket = socket(AF_INET, SOCK_STREAM)

        print("Connecting to " + str(server_ip) + " on port " + str(server_port) + "...")
        client_socket.connect(server_address)
        log = open('Logs/client_two_LOG.txt', 'a')
        log.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(server_ip) + ' ' + str(server_port) + ' ')

        strsend = input('Enter message: ')
        if strsend == '\\server':
            setServer()

        client_socket.send(str.encode(strsend))
        log.write(strsend + ' ')

        data = client_socket.recv(1024).decode()
        print(str(data))
        log.write(str(data) + '\n')
        log.close()

        client_socket.close()

except KeyboardInterrupt:
    print('Client shutting down...')
    client_socket.close()
    sys.exit(0)