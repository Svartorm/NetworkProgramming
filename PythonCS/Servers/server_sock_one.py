import socket as s
import select as sel
import sys
import time

#### Functions ####

def process(data):
    try:
        a = int(data[0])
        b = int(data[2])
        op = data[1]

        switch = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a / b,
            '%': a % b,
            '^': a ** b
        }

        return switch.get(op, 'Invalid operator')
    except:
        return 'Invalid input'

#### Main ####

server_address = ('localhost', 5000)
server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
print('Server started on', server_address, 'and listening for connections...\n')

inputs = [server_socket]

try:
    while True:
        readable, writable, exceptional = sel.select(inputs, [], [])
        for sock in readable:
            if sock is server_socket:
                client_socket, client_address = sock.accept()
                inputs.append(client_socket)
                print('Connection from', client_address, 'to', server_address, 'established.\n')
            else:
                data = sock.recv(1024).decode()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(timestamp, str(data))

                log = open('Logs/server_sel_one_LOG.txt', 'a')
                log_cache = timestamp + ' ' + str(client_address[0]) + ' ' + str(client_address[1]) + ' ' + str(data)
                log.write(log_cache + '\n')
                log.close()

                if str(data):
                    if data == '/help':
                        sock.send(str.encode('---------------------\n' 
                                            + 'Commands:\n' 
                                            + '/forcequit - Force quit the server\n' 
                                            + '/asklog - Ask for the log file\n' 
                                            + '---------------------\n'))
                    elif data == '/forcequit':
                        client_socket.close()
                        raise KeyboardInterrupt
                    elif data == '/disconnect':
                        client_socket.close()
                        sock.close()
                        inputs.remove(sock)
                    elif data == '/asklog':
                        log = open('Logs/server_sel_one_LOG.txt', 'r')
                        log_data = log.read()
                        sock.send(str.encode('---------------------\n' + log_data + '---------------------\n'))
                        log.close()
                    else:
                        res = process(str(data))
                        if res == 'Invalid input' or res == 'Invalid operator':
                            sock.send(str.encode('---------------------\n' + str(res) + ' Please try again.\n' + '---------------------\n'))
                        else:
                            sock.send(str.encode(str(server_address) + ' ' + str(data) + ' = ' + str(res) + '\n'))
                else:
                    sock.close()
                    inputs.remove(sock)

except KeyboardInterrupt:
    print('Server shutting down...')
    server_socket.close()
    sys.exit(0)

