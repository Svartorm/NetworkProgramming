import socket as s
import select as sel
import sys

server_address = ('localhost', 5000)
server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

inputs = [server_socket]

try:
    while True:
        readable, writable, exceptional = sel.select(inputs, [], [])
        for sock in readable:
            if sock is server_socket:
                client_socket, client_address = sock.accept()
                inputs.append(client_socket)
            else:
                data = sock.recv(1024).decode()
                print(str(sock.getpeername()) + ' said: ' + data)

                if str(data):
                    sock.send(data.encode())
                else:
                    sock.close()
                    inputs.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)