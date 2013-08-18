import sys
sys.path.append("../")

import sqlite

def tell(conn, msg):
    if len(msg.text.split()) > 2:
        message = ' '.join(msg.text.split()[2:])
        to = msg.text.split()[1]
        frm = msg.user

        rowid = sqlite.set("INSERT INTO irc_tell (`from`, `to`, `message`) VALUES (?, ?, ?)", (frm, to, message))
        conn.send('PRIVMSG %s :I will tell %s that when %s is here.\r\n' % (msg.channel, to, to))
    else:
        usage = 'Gebruik: !tell naam tekst'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))

def active(conn, msg):
    rows, count = sqlite.get('SELECT * FROM irc_tell WHERE `to`=?', (msg.user,))
    for row in rows:
        conn.send('PRIVMSG %s :%s: [%s] %s: %s\r\n' % (msg.channel, row[3], row[1], row[2], row[4]))
        count = sqlite.set('DELETE FROM irc_tell WHERE `id`=?', (row[0],))
