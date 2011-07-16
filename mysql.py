import settings
import MySQLdb as sql
import sys

#CREATE TABLE  `irc_tell` (
#         `id` INT( 5 ) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
#         `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
#         `from` VARCHAR( 30 ) NOT NULL ,
#         `to` VARCHAR( 30 ) NOT NULL ,
#         `message` TEXT NOT NULL
#    ) ENGINE = MYISAM ;
#
#CREATE TABLE  `irc_quote` (
#         `id` INT( 5 ) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
#         `quote` TEXT NOT NULL
#    ) ENGINE = MYISAM ;

try:
    conn = sql.connect(settings.sql_HOST, settings.sql_USER, settings.sql_PASS, settings.sql_DB)

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    
    data = cursor.fetchone()

    cursor.close()
    conn.close()
                                
except sql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

print "Database version : %s " % data
