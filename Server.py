'''
Peter Eckelmann
pje279
cs4850 Lab 3 v1
11/18/2017
Program Description:
    Server side of the chat room program. Uses sockets to connect with the client. It 
    waits until it receives a connection from the client if there is not one already. 
    When it has a connection it interprets the messages/commands it receives from the 
    client. If the quit command, ':q' is received, the server sends a message that it 
    is shutting down, and then closes the connection and quits. Otherwise, it will split 
    the message it received by white spaces, ' '. After that it checks the results against 
    the valid commands, as well as checking that the parameters needed for said commands 
    were included. If not, it informs the client that the command was unknown, or used 
    improperly. Otherwise if it's a valid command with the correct number of parameters, 
    it then goes through the remaining validation that may be needed for the given 
    command, and responds appropriately.
'''
import socket
import json

users = json.load(open('Users.json'))

sock = socket.socket()
host = socket.gethostname()
port = 10952
sock.bind((host, port))

sock.listen(5)
conn = None

currUser = ''

while (True):
    if (conn is None):
        # Halts
        print ('[Waiting for connection...]')
        conn, addr = sock.accept()
        print ('Got connection from', addr)
    ### End if conn is None:
    else:
        # Halts
        msg = (conn.recv(1024)).decode('utf-8')

        if (msg == ':q'):
            print('Shutting down.')

            conn.sendall(b'Shutting down server.')
            conn.close()

            with open('Users.json', 'w') as outfile: 
                json.dump(users, outfile)
            break
        ### End if (msg == ':q'):
        else:
            cmd = msg.split()
            
            if (len(cmd) == 3 and cmd[0] == 'login'):
                if currUser != '':
                    response = 'User ' + currUser + ' is already logged in. Please logout first if you wish to login as a differnt user.'
                    conn.sendall(response.encode('utf-8'))
                ### End if currUser != '':
                else:
                    for user in users:
                        if (user['UserID'] == cmd[1] and user['Password'] == cmd[2]):
                            response = 'Server: ' + user['UserID'] + ' joins.'
                            currUser = user['UserID']
                            conn.sendall(response.encode('utf-8'))

                            print(currUser + ' login.')
                            break
                        ### End if user['UserID'] == cmd[1] and user['Password'] == cmd[2]:
                    ### End for user in users:

                    if (currUser == ''):
                        conn.sendall(b'Incorrect UserID/Password.')
                    ### End (if currUser == ''):
                ### End else:
            ### End if (cmd[0] == 'login'):
            elif (len(cmd) == 3 and cmd[0] == 'newuser'):
                createNewUser = True

                for user in users:
                    if (user['UserID'] == cmd[1]):
                        response = 'Server: ' + user['UserID'] + ' already exists. Please try a different username.'
                        conn.sendall(response.encode('utf-8'))
                        createNewUser = False
                        break
                    ### End if (user['UserID'] == cmd[1] and user['Password'] == cmd[2]):
                ### End for user in users:

                if (createNewUser == True):
                    if (len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8):
                        users.append({'UserID' : cmd[1], 'Password' : cmd[2]})
                        response = 'User ' + cmd[1] + ' created successfully.'
                        conn.sendall(response.encode('utf-8'))
                    ### End if (len(cmd[1]) < 32 or (len(cmd[2] >= 4 and len(cmd[2]) <= 8))):
                    else:
                        conn.sendall(b'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.')
                    ### End else:
                ### End if (createNewUser != False):
            ### End elif (cmd[0] == 'newuser'):
            elif (len(cmd) > 0 and cmd[0] == 'send'):
                if (currUser == ''):
                    conn.sendall(b'Denied. Please login in first.')
                ### End if (currUser == ''):
                else:
                    cmd.remove('send')
                    msg = ' '.join(cmd)
                    msg = currUser + ': ' + msg
                    conn.sendall(msg.encode('utf-8'))

                    print(msg)
                ### End else:
            ### End elif (cmd[0] == 'send'):
            elif (len(cmd) > 0 and cmd[0] == 'logout'):
                if (currUser == ''):
                    conn.sendall(b'No user is currently logged in.')
                ### End if (currUser == ''):
                else:
                    print(currUser + ' logout.')

                    response = 'Server: ' + currUser + ' left.'
                    conn.sendall(response.encode('utf-8'))
                    currUser = ''
                    conn = None
                ### End else:
            ### End elif (cmd[0] == 'logout'):
            else:
                conn.sendall(b'Unknown command, or incorrect usage of command. Please try again.')
            ### End else:
        ### End else:
    ### End else:
### End while (True):