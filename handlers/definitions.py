import sys
sys.path.append("../")

import mysql
import settings
import utils

def assign(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) > 2:
            word = msg.text.split()[1]
            defin = ' '.join(msg.text.split()[2:])

            rows, count = mysql.get('SELECT * FROM irc_assign WHERE word=%s', (word))

            if count > 0:
                conn.send('PRIVMSG %s :%s is already defined: %s\r\n' % (msg.channel, rows[0][1], rows[0][2]))
            else:
                rowid = mysql.set('INSERT INTO irc_assign (word, def) VALUES (%s, %s)', (word, defin))
                conn.send('PRIVMSG %s :%s added to assign list.\r\n' % (msg.channel, word))
        else:
            usage = 'Gebruik: !assign woord definitie'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een administrator zijn om dit commando te kunnen uitvoeren.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))

def reassign(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) > 2:
            word = msg.text.split()[1]
            defin = ' '.join(msg.text.split()[2:])

            rows, count = mysql.get('SELECT * FROM irc_assign WHERE word=%s', (word))

            if count == 0:
                conn.send('PRIVMSG %s :%s is not defined yet. Use !assign word def to assign it.\r\n' % (msg.channel, word))
            else:
                rowid = mysql.set('UPDATE irc_assign SET def=%s WHERE word=%s', (defin, word))
                conn.send('PRIVMSG %s :%s reassigned to:%s\r\n' % (msg.channel, word, defin))
        else:
            usage = 'Gebruik: !reassign woord definitie'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een administrator zijn om dit commando te kunnen uitvoeren.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))


def unassign(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) > 1:
            word = msg.text.split()[1]
            rowid = mysql.set('DELETE FROM irc_assign WHERE word=%s', (word))
            conn.send('PRIVMSG %s :%s unassigned.\r\n' % (msg.channel, word))
        else:
            usage = 'Gebruik: !unassign woord'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een operator zijn om dit commando te kunnen gebruiken.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))

def lijst(conn, msg):
    aantal = 10
    if len(msg.text.split()) > 1:
        getal = msg.text.split()[1]
        if getal.isdigit():
            getal = int(getal)
            if getal > 0:
                aantal = getal
            if getal > 30:
                aantal = 30

    rows, count = mysql.get('SELECT * FROM irc_assign ORDER BY id DESC', '')

    if aantal > count:
        aantal = count

    out=[]
    for row in range(0, aantal):
        out.append(rows[row][1])

    conn.send('PRIVMSG %s :Last %i assigns: %s\r\n' % (msg.channel, aantal, ', '.join(out)))

def explain(conn, msg):
     if len(msg.text.split()) > 1:
         word = msg.text.split()[1]
         rows, count = mysql.get('SELECT * FROM irc_assign WHERE word = %s', (word))
         if count != 0:
             conn.send('PRIVMSG %s :%s: %s\r\n' % (msg.channel, word, rows[0][2]))
     else:
        usage = 'Gebruik: ? woord'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
