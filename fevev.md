### Hugo FRANGIAMONE
### 2019-05-01
# Midterm Exam - Network Programming
## Description
This is a chat app that allows you to send messages to other users. It is based on the TCP protocol. User can also use the following commands to interact with the server. 

List of implementation success:
- [x] Chat with other users
- [x] LIST command
- [x] UPLOAD command
- [x] DOWNLOAD command
- [ ] SENDALL command
- [x] DOWNZIP command

## Source Code Explanation
### Client
Client use a multi-threaded architecture. The main thread is used to send messages to the server. The second thread is used to receive messages from the server. Before sending a message, the client call `commandHandler` to check if the message is a command. If it is, the client will execute the command. If not, the client will send the message to the server. 
```python
def send_msg(sock):
    while True:
        data = sys.stdin.readline()

        #§ If the user types a command -> handle it has a command
        #§ Else -> send it as a message
        if not commandHandler(sock, data):
            sock.send(data.encode())
            sys.stdout.write('<You> ')
            sys.stdout.write(data)
            sys.stdout.flush()
```
Each command is handled by a function. The function returns `True` if the command is handled, `False` otherwise. 
```python
def getFilesList(sock):
    """
    Get the list of files in the server shared folder
    @param sock: The socket that will be used to send the command
    @return: True if the command was sent successfully, False otherwise
    """
    try:
        sock.send('LIST'.encode())
        response = sock.recv(2048).decode()
        print(response)
        return True
    except:
        return False

### ........

def commandHandler(sock, data):
    """
    This function handles the commands that the user types in the console
    @param data: The data that the user typed in the console
    @return: True if the data is a command, False otherwise
    """
    data = data.split(' ')
    print(data)
    head = data[0].strip()
    if head == 'QUIT': #µ Quit the program
        print('Closing the connection')
        server.close()
        sys.exit()
        return True
    elif head == 'LIST': #µ List all available files
        if not getFilesList(sock):
            print('Error: Could not get the files list')
        return True
    elif head == 'DOWNLOAD': #µ Get a file from the server
        if not downloadFile(sock, data[1].strip()):
            print('Error: Could not download the file')
        return True
    elif head == 'UPLOAD': #µ Upload a file to the server
        if not uploadFile(sock, data[1].strip()):
            print('Error: Could not upload the file')
        return True
    elif head == 'SENDALL': #µ Send a file from server shared folder to all users
        if not sendAll(sock, data[1].strip()):
            print('Error: Could not send the file to all users')
        return True
    elif head == 'DOWNZIP': #µ Download all files from the server on .zip format
        if not downloadZip(sock):
            print('Error: Could not download the files')
        return True
    elif head == 'HELP': #µ Show all available commands
        print('Available commands:')
        print('QUIT: Close the connection')
        print('LIST: List all available files')
        print('DOWNLOAD: Download a file')
        print('UPLOAD: Upload a file')
        print('SENDALL: Send a file from server shared folder to all users')
        print('DOWNZIP: Download all files from the server on .zip format')
        return True
    return False
```
### Server
The server is also multi-threaded. The main thread is used to accept new connections. Each new connection is handled by a new thread. 
Upon receiving a message, the server will check if the message is a command. If it is, the server will execute the command. If not, the server will broadcast the message to all connected clients. 
```python
message = conn.recv(2048).decode()
if message:
    print(f'Message received: {message}')
    #§ If the user types a command -> handle it has a command
    #§ Else -> send it as a message
    if not commandHandler(conn, message):
        print ('<' + addr[0] + '> ' + message)
        message_to_send = '<' + addr[0] + '> ' + message
        broadcast(message_to_send, conn)
```
```python
def commandHandler(sock, msg):
	"""
	Handle the commands sent by the client
	@param sock: The socket that will be used to send the command
	@param command: The command to handle
	@return: True if the command was sent successfully, False otherwise
	"""
	req = msg.split(SEP)
	print(f'Request received: {req}')
	cmd = req[0]
	print(f'Command received: {cmd}')

	if cmd == 'LIST':
		dir_list = os.listdir('./shared') #!!! Doesn't work
		print('Files in the server shared folder: ', dir_list)

		if not dir_list:
			res = 'Server shared folder (SSF) is empty'
		else:
			res = 'Files in the server shared folder: \n'
			for file in dir_list:
				res += f'\t-> {file}\n'
		print('Sending response: ', res)
		sock.send(res.encode())
		return True
	elif cmd == 'DOWNLOAD':
		filename = req[1]
		try:
			with open(filename, 'rb') as f:
				while True:
					bytes_read = f.read(2048)
					if not bytes_read:
						break
					sock.send(bytes_read)
				sock.send('EOF'.encode())
			f.close()
			sock.send('File downloaded successfully'.encode())
			return True
		except:
			sock.send('File not found'.encode())
			return False
	elif cmd == 'UPLOAD':
		filename = req[1]
		try:
			with open(filename, 'wb') as f:
				while True:
					bytes_read = sock.recv(2048)
					if bytes_read == 'EOF'.encode():
						break
					if not bytes_read:
						break
					f.write(bytes_read)
			f.close()
			print('File uploaded successfully')
			return True
		except:
			sock.send('Error when uploading the file'.encode())
			return False
	elif cmd == 'DOWNZIP':
		file = "shared.zip"  # zip file name
		directory = "shared"
		with ZipFile(file, 'w') as zip:
			for path, directories, files in os.walk(directory):
				for file in files:
					file_name = os.path.join(path, file)
					zip.write(file_name) # zipping the file
			print('File zipped successfully')
			while True:
				bytes_read = f.read(2048)
				if not bytes_read:
					break
				sock.send(bytes_read)
			sock.send('EOF'.encode())
		f.close()
		sock.send('File downloaded successfully'.encode())

		return True
	return False
```
## Usage
### Server
Start the server. It must have a `./shared` folder to store the files.
### Client
Start each client in a different directory. 