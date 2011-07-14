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

modes = { 'owner': '+q', 'o': '+q',
          'deowner': '-q', 'do': '-q',
          'protected': '+p', 'protect': '+p', 'p': '+p',
          'deprotected': '-p', 'deprotect': '-p', 'dp': '-p',
          'operator': '+o', 'op': '+o',
          'deoperator': '-o', 'deop': '-o', 'dop': '-o',
          'halfop': '+ho', 'ho': '+ho',
          'dehalfop': '-ho', 'dho': '-ho',
          'voice': '+v', 'v': '+v',
          'devoice': '-v', 'dv': '-v',
          'ban': '+b', 'b': '+b',
          'unban': '-b', 'b': '-b',
        }

def changeMode(channel, cmd, user):
    print 
    if cmd[0] in modes:
        if len(cmd) > 1:
            wie = cmd[1]
        else:
            wie = user
        conn.send('MODE '+channel+' '+modes[cmd[0]]+' '+wie+'\r\n')

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
        if user == settings.OWNER: # Op only functions!
            if cmd[0] in modes:
                changeMode(channel, cmd, user)
            
            if len(cmd) > 1: # We need an argument here!
                if cmd[0] == 'topic':
                    conn.send('TOPIC '+channel+' :'+msg[7:]+'\r\n')

                if cmd[0] == 'kick' or cmd[0] == 'k':
                    conn.send('KICK '+channel+' '+user+'\r\n')

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
