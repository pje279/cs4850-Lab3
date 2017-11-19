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

while True:
    if conn is None:
        # Halts
        print ('[Waiting for connection...]')
        conn, addr = sock.accept()
        print ('Got connection from', addr)
    ### End if conn is None:
    else:
        # Halts
        #print ('[Waiting for response...]')
        msg = (conn.recv(1024)).decode('utf-8')

        if msg == ':q':
            conn.sendall(b'Shutting down server.')
            conn.close()

            with open('Users.json', 'w') as outfile: 
                json.dump(users, outfile)
            break
        ### End if msg == ':q':
        else:
            cmd = msg.split()
            #print(len(cmd))
            if len(cmd) == 3 and cmd[0] == 'login':
                if currUser != '':
                    response = 'User ' + currUser + 'is already logged in. Please logout first if you wish to login as a differnt user.'
                    conn.sendall(response.encode('utf-8'))
                ### End if currUser != '':
                else:
                    for user in users:
                        if user['UserID'] == cmd[1] and user['Password'] == cmd[2]:
                            response = 'Server: ' + user['UserID'] + ' joins.'
                            currUser = user['UserID']
                            conn.sendall(response.encode('utf-8'))
                            break
                        ### End if user['UserID'] == cmd[1] and user['Password'] == cmd[2]:
                    ### End for user in users:

                    if currUser == '':
                        conn.sendall(b'Incorrect UserID/Password.')
                    ### End if currUser == '':
                ### End else:
            ### End if cmd[0] == 'login':
            elif len(cmd) == 3 and cmd[0] == 'newuser':
                createNewUser = True

                for user in users:
                    if user['UserID'] == cmd[1]:
                        response = 'Server: ' + user['UserID'] + ' already exists. Please try a different username.'
                        conn.sendall(response.encode('utf-8'))
                        createNewUser = False
                        break
                    ### End if user['UserID'] == cmd[1] and user['Password'] == cmd[2]:
                ### End for user in users:

                if createNewUser == True:
                    if len(cmd[1]) < 32 and len(cmd[2]) >= 4 and len(cmd[2]) <= 8:
                        users.append({'UserID' : cmd[1], 'Password' : cmd[2]})
                        response = 'User ' + cmd[1] + ' created successfully.'
                        conn.sendall(response.encode('utf-8'))
                    ### End if len(cmd[1]) < 32 or (len(cmd[2] >= 4 and len(cmd[2]) <= 8)):
                    else:
                        conn.sendall(b'The length of the UserID should be less than 32, and the length of the Password should be between 4 and 8 characters.')
                    ### End else:
                ### End if createNewUser != False:
            ### End elif cmd[0] == 'newuser':
            elif len(cmd) > 0 and cmd[0] == 'send':
                if currUser == '':
                    conn.sendall(b'Denied. Please login in first.')
                ### End if currUser == '':
                else:
                    cmd.remove('send')
                    msg = ' '.join(cmd)
                    msg = currUser + ': ' + msg
                    conn.sendall(msg.encode('utf-8'))
                ### End else:
            ### End elif cmd[0] == 'send':
            elif len(cmd) > 0 and cmd[0] == 'logout':
                if currUser == '':
                    conn.sendall(b'No user is currently logged in.')
                ### End if currUser == '':
                else:
                    response = 'Server: ' + currUser + ' left.'
                    conn.sendall(response.encode('utf-8'))
                    currUser = ''
                    conn = None
                ### End else:
            ### End elif cmd[0] == 'logout':
            else:
                conn.sendall(b'Unknown command, or incorrect usage of command. Please try again.')
            ### End else:
        ### End else:
        #msg = c.recvfrom(msg.decode('utf-8'))
        print (msg)
        #msg = input("Enter something to this client: ")
        #conn.sendall(msg.encode('utf-8'))
    ### End else:
### End while True: