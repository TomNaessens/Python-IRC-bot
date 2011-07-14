import sys
import socket
import string
import os
import settings

conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(HOST, PORT):
    conn.connect((HOST, PORT))
    conn.send('NICK '+NICK+'\r\n')
    conn.send('USER '+IDENT+' '+HOST+' * :'+REALNAME+'\r\n')

    initialPing()

    conn.send('PRIVMSG NickServ IDENTIFY '+PASS+'\r\n')
    conn.send('JOIN '+CHANNEL+'\r\n')

def sendPing(data):
    conn.send('PONG '+data.split()[1]+'\r\n')
    print 'PONG'

def initialPing():
    while True:
        data = conn.recv(4096)
        print data
        if data.split()[0] == 'PING':
            sendPing(data)
            print 'Initial PONG sent'
            break

def parseMessage(data):
    print ''

def listen():
    while True:
        data = conn.recv(4096)
        print data
        if data.split()[0] == 'PING':
            sendPing(data)
        if data.find('PRIVMSG') != -1:
            parseMessage(data)

connect(HOST, PORT)
listen()
