### Hugo Frangiamone -Lisa Bourlier
### 2019-09-17

## Network programming
# Challenge 1

## Introduction
This is the first challenge of the PythonClientServer course. The goal of this challenge is to create a simple TCP server and client. The server will listen for incoming connections and the client will connect to the server. The client will send a simple operation (e.g. "2+2") and the server will return the result of the operation (e.g. "4").

## Requirements
- The server must be able to handle multiple clients at the same time.
- The server must detect errors in the client's request and return an error message.

## Solutions
### Handle basic commands from client
The server detect specific messages from the clients, executing the proper response : 
```python
if data == '/help':
    sock.send(str.encode('---------------------\n' 
                        + 'Commands:\n' 
                        + '/forcequit - Force quit the server\n' 
                        + '/asklog - Ask for the log file\n' 
                        + '---------------------\n'))
elif data == '/forcequit':
    client_socket.close()
    raise KeyboardInterrupt
elif data == '/disconnect':
    client_socket.close()
    sock.close()
    inputs.remove(sock)
elif data == '/asklog':
    log = open('Logs/server_sel_one_LOG.txt', 'r')
    log_data = log.read()
    sock.send(str.encode('---------------------\n' + log_data + '---------------------\n'))
    log.close() 
```

### Process client's request
In order to compute the client's request, the server must must convert the first and last char of the string into integers and parse the operator. Finally, it must compute the result of the operation and send it back to the client. The following code shows how to do this:
```python
def process(data):
    try:
        a = int(data[0])
        b = int(data[2])
        op = data[1]

        switch = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a / b,
            '%': a % b,
            '^': a ** b
        }

        return switch.get(op, 'Invalid operator')
    except:
        return 'Invalid input'
```
```python
res = process(str(data))
if res == 'Invalid input' or res == 'Invalid operator':
    sock.send(str.encode('---------------------\n' + str(res) + ' Please try again.\n' + '---------------------\n'))
else:
    sock.send(str.encode(str(server_address) + ' ' + str(data) + ' = ' + str(res) + '\n'))
```
