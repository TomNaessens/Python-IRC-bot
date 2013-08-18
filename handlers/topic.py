import sys
sys.path.append("../")

import sqlite
import settings
import utils

def topic(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) > 1:
            topic = ' '.join(msg.text.split()[1:])
            conn.send('TOPIC %s :%s\r\n' % (msg.channel, topic))
        else:
            usage = 'Gebruik: !topic topic'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een operator zijn om dit commando te kunnen gebruiken.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
