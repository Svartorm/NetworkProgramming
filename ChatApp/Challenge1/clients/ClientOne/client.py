import socket
import select
import sys
from threading import Thread

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'black': '\033[98m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'blink': '\033[5m',
    'reverse': '\033[7m',
    'reset': '\033[0;0m'
}
SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
try:
    server.connect((ip_address, port))
except Exception as e:
    sys.stdout.write(COLORS['red'])
    print('Connection error: ' + str(e))
    sys.stdout.write(COLORS['reset'])
    sys.exit()

##? Client login ##
sys.stdout.write(COLORS['yellow'])
sys.stdout.write('Welcome to the shtDiscord !\n')
sys.stdout.write(COLORS['reset'])
username = input('Enter username: ')
username = str(username)
server.send(username.encode())
sys.stdout.write(COLORS['yellow'])
print('You are now logged in as: ' + username)
sys.stdout.write(COLORS['reset'])
##? """""""""""" ##

currentGroup = ''

##% Message functions ##
def send_msg(sock):
    while True:
        sys.stdout.write(COLORS['reset'])
        sys.stdout.flush()
        data = input()

        if data == '':
            continue

        #§ Commands
        if data == '/quit' or data == '/exit':
            server.close()
            sys.exit()

        #§ Send message
        req = data
        if data[0] != '/' and currentGroup != '':
            req = f'{currentGroup}{SEPARATOR}{data}'
        sock.send(req.encode())

        #§ Check if message is a command
        if data[0] == '/':
            continue

        #§ Print message
        sys.stdout.write(COLORS['bold'])
        print(f'<You> {data}')
        sys.stdout.write(COLORS['reset'])

def recv_msg(sock):
    while True:
        #§ Receive message
        data = sock.recv(BUFFER_SIZE).decode()

        #§ Compute message
        data = data.split(SEPARATOR)

        if len(data) == 1: #µ Normal messages
            sys.stdout.write(COLORS['bold'])
            print(data[0])
            sys.stdout.write(COLORS['reset'])

        elif len(data) == 2 and data[0] == 'SYS': #µ System messages
            sys.stdout.write(COLORS['yellow'] + COLORS['blink'])
            print(data[1])
            sys.stdout.write(COLORS['reset'])
        
        elif len(data) == 2 and data[0] == 'ERR': #µ Error messages
            sys.stdout.write(COLORS['red'] + COLORS['bold'])
            print(data[1])
            sys.stdout.write(COLORS['reset'])
        
        elif len(data) == 2 and data[0] == 'SET': #µ Set orders from server
            currentGroup = data[1]

        elif len(data) == 3: #µ Targeted messages
            header, author, msg = data[0], data[1], data[2]
            if header == 'PV': #µ Private message
                sys.stdout.write(COLORS['purple'] + COLORS['bold'])
                print(f'<from {author}> {msg}')
                sys.stdout.write(COLORS['reset'])

            else: #µ Group message
                if header[0] != 'g' or header[1] != '\\':
                    continue
                try:
                    sys.stdout.write(COLORS['green'] + COLORS['bold'])
                    print(f'<{header} | {author}> {msg}')
                    sys.stdout.write(COLORS['reset'])

                except Exception as e:
                    sys.stdout.write(COLORS['red'])
                    print('Error receiving msg from ' + author + ': ' + str(e))
                    sys.stdout.write(COLORS['reset'])
                    continue
##% """""""""""""""" ##

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
