import settings

def kick(conn, msg):
    if msg.user == settings.irc_OWNER:
        if len(msg.text.split()) == 2:
            conn.send('KICK '+msg.channel+' '+msg.text.split()[1]+'\r\n')
        elif len(msg.text.split()) > 2:
            conn.send('KICK '+msg.channel+' '+msg.text.split()[1]+' :'+" ".join(msg.text.split()[2:])+'\r\n')
