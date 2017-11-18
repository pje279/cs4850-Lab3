#!/usr/bin/python

import socket

s = socket.socket()
host = socket.gethostname()
port = 10952
s.bind((host, port))

s.listen(5)
c = None

while True:
    if c is None:
        # Halts
        print ('[Waiting for connection...]')
        c, addr = s.accept()
        print ('Got connection from', addr)
    else:
        # Halts
        #print ('[Waiting for response...]')
        q = (c.recv(1024)).decode('utf-8')

        if q == ':q':
            c.sendall(b'Shutting down server')
            c.close()
            break
        #q = c.recvfrom(q.decode('utf-8'))
        print (q)
        #q = input("Enter something to this client: ")
        #c.send(q)
        #c.sendto(q, (host, port))
        c.sendall(q.encode('utf-8'))