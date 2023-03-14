import socket as s
import sys
import os
import threading

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

####### Functions ########
def listen():
    try:
        msg = client_socket.recv(BUFFER_SIZE).decode()
        download(msg)
    
    except:
        print('Error receiving file.\n')

def upload():
    try:
        while True:
            try:
                # Get file info
                filepath = input("File to transfer: ")

                filesize = os.path.getsize(filepath)
                filename = os.path.basename(filepath)

                # Send file info to server
                client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

                # Send file to server
                with open(filepath, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                f.close()

            except Exception as e:
                print('Error sending file. Please try again.\n')
                print(e)

            sys.stdout.write('>> ')

    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)

def download(received):
    # Receive file info from server
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    
    sys.stdout.write(f'Receiving file from client : {filename} ({filesize} bytes)\n')

    # Receive file from server
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
    f.close()
###### !Functions! #######

print('Client starting...')

server_address = ('localhost', 5000)
client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

####§ Listen to server
listener = threading.Thread(target=listen)
listener.start()

####§ Client want to send an upload request
inputHandler = threading.Thread(target=upload)
inputHandler.start()

# End of file
listener.join()
inputHandler.join()