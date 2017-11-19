'''
Peter Eckelmann
pje279
cs4850 Lab 3 v1
11/18/2017
Program Description:
    Client side of the chat room program. Uses sockets to connect with the server.
    While connected, the client can send messages/commands to the server. The connection 
    is ended if the quit command ':q' is called (shuts the server and client down), 
    or if the user logs out (and they were already logged in, can't log out if they 
    were not already logged in).
'''

import socket

sock = socket.socket()
host = socket.gethostname()
port = 10952

sock.connect((host, port))
print ('Connected to', host)

while (True):
    #z = input("Enter something for the server: ")
    msg = input('> ')
    sock.sendall(msg.encode('utf-8'))
    # Halts
    returnMsg = (sock.recv(1024)).decode('utf-8')
    print ('> ' + returnMsg)

    if (msg == ':q'):
        break
    ### End if z == ':q':
    elif (msg == 'logout' and returnMsg != 'No user is currently logged in.'):
        break
    ### End elif (msg == 'logout' and returnMsg != 'No user is currently logged in.'):
### End while (True):