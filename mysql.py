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
#
#CREATE TABLE  `ircbot`.`irc_assign` (
#        `id` INT( 5 ) NOT NULL AUTO_INCREMENT ,
#        `word` VARCHAR( 30 ) NOT NULL ,
#        `def` TEXT NOT NULL ,
#        PRIMARY KEY (  `id` ) ,
#        INDEX (  `id` )
#        ) ENGINE = MYISAM ;

# Shorter names are shorter
HOST = settings.sql_HOST
USER = settings.sql_USER
PASS = settings.sql_PASS
DB = settings.sql_DB
PORT = settings.sql_PORT

def set(query, args):
    rowid = -1

    try:
        conn = sql.connect(HOST, USER, PASS, DB, PORT)
        
        cursor = conn.cursor()
        cursor.execute(query, args)
        
        rowid = cursor.lastrowid

        conn.commit()

        cursor.close()
        conn.close()
    except sql.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1]) 
    return rowid

def get(query, args):
    rows = (-1, 'Error')
    count = 0
    try:
        conn = sql.connect(HOST, USER, PASS, DB, PORT)
        
        cursor = conn.cursor()

        if len(args) == 0:
            cursor.execute(query)
        else:
            cursor.execute(query, args)
 
        rows = cursor.fetchall()
        count = cursor.rowcount

        cursor.close()
        conn.close()
    except sql.Error, e:
        print 'Error %d: %s' % (e.args[0], e.args[1]) 

    return rows, count
