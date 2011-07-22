def topic(conn, msg):
    conn.send('TOPIC '+msg.channel+' :'+msg.text[7:]+'\r\n')
