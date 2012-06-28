import settings
import utils

def alarm(conn, msg):
    conn.send('PRIVMSG %s :QUACK QUACK QUACK\r\n' % (msg.channel))
