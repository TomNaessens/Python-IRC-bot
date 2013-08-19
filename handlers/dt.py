import sys
sys.path.append("../")

import sqlite
import settings
import utils

def dt(conn, msg):
    if len(msg.text.split()) > 2:
        naam = msg.text.split()[1]
        error = ' '.join(msg.text.split()[2:])
        rowid = sqlite.set('INSERT INTO irc_dt (name, error) VALUES (?, ?)', (naam, error,))
        conn.send('PRIVMSG %s :DT-fout %i added!\r\n' % (msg.channel, rowid))
    else:
        parts = msg.text.split()
        if len(parts) == 1:
            rows, count = sqlite.get('SELECT * FROM irc_dt ORDER BY RANDOM()', ())

            if count != 0:
                conn.send('PRIVMSG %s :DT-fout %i: [%s] %s\r\n' % (msg.channel, rows[0][0], rows[0][1], rows[0][2]))

        elif parts[1].isdigit():
            rows, count = sqlite.get('SELECT * FROM irc_dt WHERE id=?', (parts[1],))

            if count != 0:
                conn.send('PRIVMSG %s :DT-fout %i: [%s] %s\r\n' % (msg.channel, rows[0][0], rows[0][1], rows[0][2]))

        else:
            rows, count = sqlite.get('SELECT * FROM irc_dt WHERE name=? ORDER BY RANDOM()', (parts[1],))

            if count != 0:
                conn.send('PRIVMSG %s :DT-fout: %s heeft in totaal al %i DT-fouten gemaakt\r\n' % (msg.channel, rows[0][1], count))
            else:
                conn.send('PRIVMSG %s :DT-fout: %s heeft nog geen DT-fouten gemaakt\r\n' % (msg.channel, parts[1]))



def list(conn, msg):

    aantal = 5
    if len(msg.text.split()) > 1:
        getal = msg.text.split()[1]
        if getal.isdigit():
            getal = int(getal)
            if getal > 0:
                aantal = getal
            if getal > 15:
                aantal = 15

    rows, count = sqlite.get('SELECT name, COUNT(*) FROM `irc_dt` GROUP BY name ORDER BY COUNT(*) DESC', ())
    conn.send('PRIVMSG %s :Nr.: Naam - Aantal\r\n' % (msg.channel))

    if count < aantal:
        aantal = count

    conn.send('PRIVMSG %s :DT-fouten top %i:\r\n' % (msg.channel, aantal))
    for row in range(0, aantal):
        conn.send('PRIVMSG %s :  %i: %s - %s\r\n' % (msg.channel, (row+1), rows[row][0], rows[row][1]))
