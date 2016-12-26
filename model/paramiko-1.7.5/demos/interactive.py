#coding:utf-8

import socket
import sys
import time
import MySQLdb
# Windows does not have termios...

try:

    import termios

    import tty

    has_termios = True

except ImportError:

    has_termios = False

def interactive_shell(chan,hostname,username,ops_user):

    if has_termios:

        posix_shell(chan,hostname,username,ops_user)

    else:

        windows_shell(chan)

###########
def log_to_db(loginfo):
  try:
    conn = MySQLdb.connect(host = "10.100.0.200", user = "root", passwd = "wind2010",db = "opdb")
    cursor = conn.cursor()
    sql = '''insert into oplog(id,ops_user,date_time,op_time,login_ip,login_by,exec_command) values(%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sql,loginfo)
    conn.commit()
    cursor.close()
    conn.close()
  except Exception as e:
    print e



############
def posix_shell(chan,hostname,username,ops_user):

    import select

    

    oldtty = termios.tcgetattr(sys.stdin)
    date = time.strftime('%Y-%m-%d')
    f=file('/tmp/audit_%s_%s.log' % (ops_user,date),'ab+') 

    try:

        tty.setraw(sys.stdin.fileno())

        tty.setcbreak(sys.stdin.fileno())

        chan.settimeout(0.0)

        records = []   #定义一个空列表

        while True:

            r, w, e = select.select([chan, sys.stdin], [], [])

            if chan in r:

                try:

                    x = chan.recv(1024)

                    if len(x) == 0:

                        print '\r\n*** EOF\r\n',

                        break

                    sys.stdout.write(x)

                    sys.stdout.flush()

                except socket.timeout:

                    pass

            if sys.stdin in r:          #屏幕接收

                x = sys.stdin.read(1)    #每次只接收一个字符

                records.append(x)

                if x == '\r':         #每个命令输完回车都有一个\r

                    c_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    date_time = time.strftime('%Y%m%d')
                    cmd = ''.join(records).replace('\r','\n')#\r win换行,\n linux的换行
                    log = '%s |ops_user: %s| %s |login by: %s | %s' %(c_time,ops_user,hostname,username,cmd)
                    loginfo = ('',ops_user,date_time,c_time,hostname,username,cmd)
                    f.write(log)    
                    f.flush() 
                    log_to_db(loginfo)
                    records = []
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        f.close()

    

# thanks to Mike Looijmans for this code

def windows_shell(chan):

    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

        

    def writeall(sock):

        while True:

            data = sock.recv(256)

            if not data:

                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')

                sys.stdout.flush()

                break

            sys.stdout.write(data)

            sys.stdout.flush()

        

    writer = threading.Thread(target=writeall, args=(chan,))

    writer.start()

        

    try:

        while True:

            d = sys.stdin.read(1)

            if not d:

                break

            chan.send(d)

    except EOFError:

        # user hit ^Z or F6

        pass
