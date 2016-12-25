import MySQLdb  



def mysql_query(ops_user):

  try:  
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "123456", db = "opdb")  
    cursor = conn.cursor ()
    cmd = '''SELECT * FROM userinfo where username = "%s"''' % ops_user
    cursor.execute (cmd)  
    rows = cursor.fetchall() 
    lst = []
    for row in rows: 
       print row 
       lst.append(row[2])
    print lst
  
#print "Number of rows returned: %d" % cursor.rowcount  
  
#cursor.execute ("SELECT * FROM userinfo")  
#while (True):  
#    row = cursor.fetchone()  
#    if row == None:  
#        break  
#    print "%d, %s, %s, %s" % (row[0], row[1], row[2], row[3])  
      
#print "Number of rows returned: %d" % cursor.rowcount  
  
    cursor.close ()  
    conn.close ()
  except Exception as e:
    print e

mysql_query('wind')
