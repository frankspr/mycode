import MySQLdb
def log_to_db(loginfo):
  try:
    conn = MySQLdb.connect(host = "10.100.0.200", user = "root", passwd = "wind2010",db = "opdb")
    cursor = conn.cursor()
    sql = '''insert into oplog(id,ops_user,date_time,op_time,login_ip,login_by,exec_command) values(%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sql,loginfo)
    print loginfo
    conn.commit()
    cursor.close()
    conn.close()
  except Exception as e:
    print e

if __name__ == '__main__':
  aaa = ('','hjhuang','20161226','2016-12-26 17:17:20','10.100.0.55','root','free -m')
  log_to_db(aaa)
