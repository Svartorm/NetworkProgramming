import socket
from pprint import pprint
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

server_address = ('localhost', 9999)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )

##get file info (name and size)
filepath = input("enter file to transfer: ")

filename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)

## Send file info to server
client_socket.sendto(f"{filename}{SEPARATOR}{filesize}".encode(), server_address)

# Send file to server
print(f"Sending file {filename} ({filesize} bytes).")

with open(filepath, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        client_socket.sendto(bytes_read, server_address)
f.close()
client_socket.sendto('\r\nMessage received Cap\'tain\r\n'.encode(), server_address)
print(f"File {filename} sent successfully.")