#!/usr/bin/python

import socket

s = socket.socket()
host = socket.gethostname()
port = 10952

s.connect((host, port))
print ('Connected to', host)

while True:
    z = input("Enter something for the server: ")
    #s.send(z)
    #s.sendto(z.encode('utf-8'), (host, port))
    s.sendall(z.encode('utf-8'))
    # Halts
    #print ('[Waiting for response...]')
    print ((s.recv(1024)).decode('utf-8'))