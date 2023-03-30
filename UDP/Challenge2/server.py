import socket
import sys
import os
import time

SERVER_ADDRESS = ('localhost', 9999)
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SERVER_ADDRESS)

print('starting up on %s port %s' % SERVER_ADDRESS)
print('waiting to receive message')

while True:
    data, address = sock.recvfrom(BUFFER_SIZE)
    if data:
        data = data.decode()
        data = data.split(SEPARATOR)
        filename, filesize = data[0], int(data[1])
    else:
        break
    
    #µ Receive file from server
    print(f"Receiving file from {address} : {filename} ({filesize} bytes).")
    sizecount = 0
    with open(filename, "wb") as f:
        while True:
            #* Data of the packet
            bytes_read, address = sock.recvfrom(BUFFER_SIZE)
            if not bytes_read:
                continue
            if bytes_read.decode() == 'EOF':
                break
            f.write(bytes_read)
            sock.sendto('PKOK'.encode(), address)
            sizecount += len(bytes_read)

    
    f.close()
    print(f"Received {round(sizecount*100/filesize, 2)}% of file ({sizecount} of {filesize} bytes).")