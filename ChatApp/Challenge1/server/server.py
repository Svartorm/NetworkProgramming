import socket
import select
import sys
import threading
from group import Group

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 2048

print('Starting server...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
list_of_users = []
list_of_groups = []

print(f'Server started and listening on ({ip_address}|{port})')

def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(BUFFER_SIZE).decode()
            if message:
                ##§ Commands ##
                if message[0] == '/':
                    msg = message.split(' ')
                    res, tar = None, None

                    #µ User commands
                    if msg[0] == '/help':
                        res = help()
                        conn.send(res.encode())
                        continue
                    elif msg[0] == '/list':
                        res = list(conn, getUsername(conn))
                        conn.send(res.encode())
                        continue
                    elif msg[0] == '/private':
                        res, tar = private(msg, getUsername(conn))
                        if res is None:
                            conn.send(f'SYS{SEPARATOR}User \'{tar}\' not found'.encode())
                            continue

                    #µ Group commands
                    elif msg[0] == '/createGroup':
                        res = createGroup(msg, conn)
                        conn.send(res.encode())
                        continue
                    elif msg[0] == '/joinGroup':
                        res = joinGroup(msg, conn)
                        continue
                    elif msg[0] == '/leaveGroup':
                        res = leaveGroup(msg, conn)
                        conn.send(res.encode())
                        continue

                    else:
                        conn.send(f'ERR{SEPARATOR}Command not found'.encode())
                        continue

                    broadcast(res, conn, tar) #? Send the result to the target
                
                ##§ messages ##
                else:
                    message = message.split(SEPARATOR)
                    username = getUsername(conn)

                    if len(message) == 1: #µ Normal message
                        print(f'>> <{username}> send to \'GlobalChat\' : {message[0]}')
                        message_to_send = f'<{username}> {message[0]}'
                        broadcast(message_to_send, conn)

                    elif len(message) == 2: #µ Group message
                        groupname = message[0]
                        group = getGroup(groupname)
                        
                        if group is None:
                            conn.send(f'ERR{SEPARATOR}Group \'{groupname}\' not found'.encode())
                            continue

                        message = message[1]
                        print(f'>> <{username}> send to \'{groupname}\' : {message}')
                        message_to_send = f'g\{groupname}{SEPARATOR}{username}{SEPARATOR}{message}'
                        broadcast(message_to_send, conn, group.members)

            else:
                remove(conn)
        except:
            continue

###* Utils ###
def broadcast(message, connection, targets=list_of_clients):
    for clients in targets:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
    for co, username in list_of_users:
        if co == connection:
            print(f'{username} disconnected')
            list_of_users.remove((co, username))

def login(conn, addr):
    username = conn.recv(BUFFER_SIZE).decode()
    if (conn, username) not in list_of_users:
        list_of_users.append((conn, username))
    print(f'{addr} is now logged in as {username}')

def getUsername(conn):
    for co, username in list_of_users:
        if conn == co:
            return username

def getConn(username):
    for co, user in list_of_users:
        if username == user:
            return co

def getGroup(name):
    for group in list_of_groups:
        if group.name == name:
            return group
    return None
###* Utils ###
###% Commands functions ###
def help():
    print('Help command')
    return 'SYS<SEPARATOR>Help command'

def list(conn, user):
    print(f'List command from {user}')
    #?TODO: Find groups w/ user
    res = f'SYS{SEPARATOR}---- List of users: ----\n'
    for co, username in list_of_users:
        if co != conn:
            res += f'|-> {username}\n'
        else:
            res += f'|-> {username} (You)\n'
    res += f'------------------------'

    return res

def private(msg, username):
    print('Private command')
    target = msg[1]
    message = ' '.join(msg[2:])
    connection = getConn(target)
    if connection:
        print(f'>> <{username}> send to \'{target}\' : {message}')
        return f'PV{SEPARATOR}{username}{SEPARATOR}{message}', [connection]
    else:
        return None, target
    
def createGroup(msg, user):
    try:
        name = msg[1]
        group = Group(name, user)
        list_of_groups.append(group)
        user.send(f'SET{SEPARATOR}{name}'.encode())
        return f'SYS{SEPARATOR}Group \'{name}\' created'
    except Exception as e:
        print(e)
        return f'ERR{SEPARATOR}Error: Group \'{name}\' could not be created'

def joinGroup(msg, user):
    try:
        name = msg[1]
        group = getGroup(name)
        
        if group is None:
            return f'ERR{SEPARATOR}Group \'{name}\' not found'
        
        group.member.append(user)
        user.send(f'SET{SEPARATOR}{name}'.encode())
        return f'SYS{SEPARATOR}You joined group \'{name}\''
    
    except Exception as e:
        print(e)
        return f'ERR{SEPARATOR}Error: Group \'{name}\' could not be joined'

def leaveGroup(msg, user):
    try:
        name = msg[1]
        group = getGroup(name)
        
        if group is None:
            return f'ERR{SEPARATOR}Group \'{name}\' not found'
        
        group.member.remove(user)
        user.send(f'SET{SEPARATOR}'.encode())
        return f'SYS{SEPARATOR}You joined group \'{name}\''
    
    except Exception as e:
        print(e)
        return f'ERR{SEPARATOR}Error: Group \'{name}\' could not be joined'

###% """"""""""""""""""" ###

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(f'{addr} connected')
    login(conn, addr)
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()