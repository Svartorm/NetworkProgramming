import socket as s
import sys

print('Client starting...')

server_address = ('localhost', 5000)
client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        filename = str(input())

        try:
            flux = open(filename, 'r')
            # read all lines of the file
            lines = flux.readlines()
            # close the file
            flux.close()

            for line in lines:
                msg = line.rstrip()
                client_socket.send(msg.encode())
                sys.stdout.write(client_socket.recv(1024).decode())
        
        except:
            sys.stdout.write('---------------------\n' + 'Invalid file name. Please try again.\n' + '---------------------\n')

        sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)