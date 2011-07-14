import sys
import socket
import string
import settings

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(HOST, PORT, NICK, IDENT, REALNAME, PASS, CHANNEL):
    conn.connect((HOST, PORT))
    conn.send('NICK '+NICK+'\r\n')
    conn.send('USER '+IDENT+' '+HOST+' * :'+REALNAME+'\r\n')

    initialPing() # Wait for initial ping

    conn.send('PRIVMSG NickServ IDENTIFY '+PASS+'\r\n')
    conn.send('JOIN '+CHANNEL+'\r\n')

def sendPing(ping):
    conn.send('PONG '+ping+'\r\n')
    print 'PONG'

def initialPing():
    while True:
        data = conn.recv(4096)
        print data
        if data.split()[0] == 'PING':
            sendPing(data.split()[1])
            print 'Initial PONG sent'
            break

def parseMessage(data):
    full = data[1:]
    info = full.split(':')[0].rstrip()
    msg = full.split(':')[1]
    user = info.split('!')[0]
    channel = info.split()[2]
    char = msg[:1]

    if msg.strip() == "Ohai, "+settings.NICK+"!":
        conn.send('PRIVMSG '+channel+' : Ohai, '+user+'!\r\n')

    if char == '!':
        cmd = msg[1:].split()
        if user == settings.OWNER:
            if cmd[0] == 'owner' or cmd[0] == 'q':
                conn.send('MODE '+channel+' +q '+cmd[1]+'\r\n')
            if cmd[0] == 'deowner' or cmd[0] == 'dq':
                conn.send('MODE '+channel+' -q '+cmd[1]+'\r\n')
            if cmd[0] == 'protected' or cmd[0] == 'p':
                conn.send('MODE '+channel+' +p '+cmd[1]+'\r\n')
            if cmd[0] == 'deprotected' or cmd[0] == 'dp':
                conn.send('MODE '+channel+' -p '+cmd[1]+'\r\n')
            if cmd[0] == 'op' or cmd[0] == 'o':
                conn.send('MODE '+channel+' +o '+cmd[1]+'\r\n')
            if cmd[0] == 'deop' or cmd[0] == 'do':
                conn.send('MODE '+channel+' -o '+cmd[1]+'\r\n')
            if cmd[0] == 'halfop' or cmd[0] == 'ho':
                conn.send('MODE '+channel+' +h '+cmd[1]+'\r\n')
            if cmd[0] == 'dehalfop' or cmd[0] == 'dho':
                conn.send('MODE '+channel+' -h '+cmd[1]+'\r\n')
            if cmd[0] == 'voice' or cmd[0] == 'v':
                conn.send('MODE '+channel+' +v '+cmd[1]+'\r\n')
            if cmd[0] == 'devoice' or cmd[0] == 'dv': 
                conn.send('MODE '+channel+' -v '+cmd[1]+'\r\n')

def listen():
    while True:
        data = conn.recv(4096)
        print data
        if data.split()[0] == 'PING':
            sendPing(data.split()[1])
        if data.find('PRIVMSG '+settings.CHANNEL) != -1:
            parseMessage(data)

connect(settings.HOST, settings.PORT, settings.NICK, settings.IDENT, settings.REALNAME, settings.PASS, settings.CHANNEL)
listen()
