def parse(data):
    full = data[1:]
    info = full.split(':')[0].rstrip()
    text = full.partition(':')[2]
    user = info.split('!')[0]
    channel = info.split()[2]
    char = text[:1]
    cmd = text[1:].split()

    return full, info, text, user, channel, char, cmd

def isadmin(conn, msg):
    conn.send('WHOIS %s\r\n' % msg.user)
    
    data = conn.recv(4096)
    char = data[data.find(msg.channel)-1]

    return char == '~' or char == '@'
