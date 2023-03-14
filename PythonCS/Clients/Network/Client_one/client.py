import socket as s
import sys
import os
import threading
#import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

####### Functions ########
def listen():
    try:
        while True:
            msg = client_socket.recv(BUFFER_SIZE).decode()
            print(f"\nReceived >> {msg}")
            download(msg)
    
    except Exception as e:
        print('Error receiving file.')
        print(e)

def upload():
    try:
        while True:
            try:
                # Get file info
                filepath = input("File to transfer: ")
                
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)
                

                # Send file info to server
                client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

                # Send file to server
                print(f"Sending file {filename} ({filesize} bytes).")
                #progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
                with open(filepath, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                        #progress.update(len(bytes_read))
                f.close()
                print(f"File {filename} sent successfully.")

            except Exception as e:
                print('Error sending file. Please try again.')
                print(e)

            sys.stdout.write('>> ')

    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)

def download(received):
    # Receive file info from server
    source, filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    
    #progress = tqdm.tqdm(range(filesize), f"Receiving file from {source} : {filename} ({filesize} bytes).", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)

    # Receive file from server
    print(f"Receiving file from {source} : {filename} ({filesize} bytes).")
    with open(filename, "wb") as f:
        while True:
            if filesize < 1:
                break
            bytes_read = client_socket.recv(BUFFER_SIZE)
            f.write(bytes_read)
            filesize -= len(bytes_read)
            #progress.update(len(bytes_read))
    f.close()
    print(f"File {filename} received successfully.")
    sys.stdout.write('>> ')
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