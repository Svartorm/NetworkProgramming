"""
Please create a file sending simulator using UDP ( no connect(), just use send-to and recv-from) in which file are fragmented and sent using block per 1 kb.
implement client and server at different PC.

[1]: Client can pick file name that would be sent (minimum text file size 10mb)
[2]: then client send the file seqentially
[3]: after it finished sending, server and client will display how many % data is sucessfully delivered
"""

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
            bytes_read, address = sock.recvfrom(BUFFER_SIZE)
            if bytes_read.decode() == '\r\nMessage received Cap\'tain\r\n':
                break
            f.write(bytes_read)
            sizecount += len(bytes_read)
    
    f.close()
    print(f"Received {round(sizecount*100/filesize, 2)}% of file ({sizecount} of {filesize} bytes).")