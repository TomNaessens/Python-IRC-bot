import sys
import socket
import string
import quote
import settings
import kick
import utils
import privmsg

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(HOST, PORT, NICK, IDENT, REALNAME, PASS, CHANNEL):
    conn.connect((HOST, PORT))
    conn.send('NICK '+NICK+'\r\n')
    conn.send('USER '+IDENT+' '+HOST+' * :'+REALNAME+'\r\n')

    initialPing() # Wait for initial ping

    conn.send('PRIVMSG NickServ IDENTIFY '+PASS+'\r\n')
    conn.send('JOIN '+CHANNEL+'\r\n')
    conn.send('PRIVMSG '+CHANNEL+' :Quack!\r\n')

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
          'halfop': '+ho', 'hop': '+ho', 'ho': '+ho',
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

msg = privmsg.PrivMSG(':Null!Null NULL null:null')

actions = {'kick': kick.kick,
           'k': kick.kick,
           'topic': topic.topic,
           't': topic.topic
        }

def parseMessage(data):

    msg = privmsg.PrivMSG(data)

    if msg.text.find('Quack') != -1:
        conn.send('PRIVMSG '+msg.channel+' : Quack, '+msg.user+'!\r\n')

    if msg.char == '!':
        if msg.user == settings.irc_OWNER: # Op only functions!
            if msg.cmd[0] in modes:
                changeMode(msg.channel, msg.cmd, msg.user)
            
            if len(msg.cmd) > 1: # We need an argument here!
                if msg.cmd[0] == 'topic':
                    conn.send('TOPIC '+msg.channel+' :'+msg.text[7:]+'\r\n')

            if msg.cmd[0] in actions:
                actions[msg.cmd[0]](conn, msg)

        if msg.cmd[0] == 'addquote' and len(msg.cmd) > 1:
            quote.addquote(msg.text[len('addquote')+2:])

def listen(channel):
    while True:
        data = conn.recv(4096)
        print data
        if data.split()[0] == 'PING':
            sendPing(data.split()[1])
        if data.find('PRIVMSG '+channel) != -1:
            parseMessage(data)

connect(settings.irc_HOST, settings.irc_PORT, settings.irc_NICK, settings.irc_IDENT, settings.irc_REALNAME, settings.irc_PASS, settings.irc_CHANNEL)
listen(settings.irc_CHANNEL)
