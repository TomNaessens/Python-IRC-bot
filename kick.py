import settings

def kick(conn, msg):
    if msg.user == settings.irc_OWNER and len(msg.text.split()) > 1:
        conn.send('KICK '+msg.channel+' '+msg.text.split()[1]+'\r\n')
