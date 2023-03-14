import select
import socket
import os
import sys
import threading
#import tqdm

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:

            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self, self.server.accept())
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

	# close all threads
        self.server.close()
        for c in self.threads:
            c.join()
    
    def reqDL(self, source, filename, filesize):
        for c in self.threads:
            if c != source:
                c.download(source, filename, filesize)

class Client(threading.Thread):
    def __init__(self, server, client_address):
        threading.Thread.__init__(self)
        self.server = server
        self.client = client_address[0]
        self.address = client_address[1]
        self.size = 1024
        self.separator = "<SEPARATOR>"

    def run(self):
        print(f"Client connected from {self.address}.")
        
        running = 1
        while running:
            data = self.client.recv(self.size)
            print (str(self.address) + ' >> ' + str(data))

            try:
                #§ Get file information
                filename, filesize = data.decode().split(self.separator)
                filepath = 'tmp/' + filename
                fs = int(filesize)
                source = self.address

                #§ Download file from client
                #progress = tqdm.tqdm(range(filesize), f"Receiving file from {source} : {filename} ({filesize} bytes).", unit="B", unit_scale=True, unit_divisor=self.size)
                print(f"Receiving file from {source} : {filename} ({fs} bytes).")
                with open(filepath, "wb") as f:
                    while True:
                        if fs < 1:
                            break
                        bytes_read = self.client.recv(self.size)
                        f.write(bytes_read)
                        fs -= len(bytes_read)
                        #progress.update(len(bytes_read))
                f.close()
                print(f"File {filename} received from {source}.")

                #§ Request upload to other clients
                self.server.reqDL(self, filename, int(filesize))

                #§ Remove file from /tmp
                os.remove(filepath)

            except Exception as e:
                print("Error downloading file. Please try again.")
                print(e)
                #self.client.close()
                #running = 0
    
    def download(self, source, filename, filesize):
        self.client.send(f"{source.address}{self.separator}{filename}{self.separator}{filesize}".encode())
        filepath = 'tmp/' + filename

        #progress = tqdm.tqdm(range(filesize), f"Sending file to {self.address} : {filename} ({filesize} bytes).", unit="B", unit_scale=True, unit_divisor=self.size)
        print(f"Sending file to {self.address} : {filename} ({filesize} bytes).")
        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(self.size)
                if not bytes_read:
                    break
                self.client.sendall(bytes_read)
                #progress.update(len(bytes_read))
        f.close()
        print(f"File {filename} sent to {self.address}.")

if __name__ == "__main__":
    s = Server()
    print("Launching server...")
    s.run()
