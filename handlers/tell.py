import sys
sys.path.append("../")

import mysql

def tell(conn, msg):
    if len(msg.text.split()) > 2:
        message = ' '.join(msg.text.split()[2:])
        to = msg.text.split()[1]
        frm = msg.user

        rowid = mysql.set("INSERT INTO irc_tell (`from`, `to`, `message`) VALUES (%s, %s, %s)", (frm, to, message))
        conn.send('PRIVMSG %s :I will tell %s that when %s is here.\r\n' % (msg.channel, to, to))

def active(conn, msg):
    rows, count = mysql.get('SELECT * FROM irc_tell WHERE `to`=%s', (msg.user))
    for row in rows:
        conn.send('PRIVMSG %s :%s: [%s] %s: %s\r\n' % (msg.channel, row[3], row[1], row[2], row[4]))
        count = mysql.set('DELETE FROM irc_tell WHERE `id`=%s', row[0])
