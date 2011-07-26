import settings
import utils

def kick(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) == 2:
            conn.send('KICK '+msg.channel+' '+msg.text.split()[1]+'\r\n')
        elif len(msg.text.split()) > 2:
            conn.send('KICK '+msg.channel+' '+msg.text.split()[1]+' :'+" ".join(msg.text.split()[2:])+'\r\n')
        else:
            usage = 'Gebruik: !kick naam [reden] (reden is optioneel)'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een operator zijn om dit commando te gebruiken.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))


