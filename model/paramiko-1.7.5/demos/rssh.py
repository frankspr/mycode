#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import threading
import time
import traceback
import MySQLdb
import paramiko
import interactive


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
        
    for key in agent_keys:
        print 'Trying ssh-agent key %s' % hexlify(key.get_fingerprint()),
        try:
            transport.auth_publickey(username, key)
            print '... success!'
            return
        except paramiko.SSHException:
            print '... nope.'


def manual_auth(username, hostname):
    #default_auth = 'p'
    #auth = raw_input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    #if len(auth) == 0:
    #    auth = default_auth
#    if auth == 'r':
#        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
#        path = raw_input('RSA key [%s]: ' % default_path)
#        if len(path) == 0:
#            path = default_path
#        try:
#            key = paramiko.RSAKey.from_private_key_file(path)
#        except paramiko.PasswordRequiredException:
#            password = getpass.getpass('RSA key password: ')
#            key = paramiko.RSAKey.from_private_key_file(path, password)
#        t.auth_publickey(username, key)
#    elif auth == 'd':
#        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
#        path = raw_input('DSS key [%s]: ' % default_path)
#        if len(path) == 0:
#            path = default_path
#        try:
#            key = paramiko.DSSKey.from_private_key_file(path)
#        except paramiko.PasswordRequiredException:
#            password = getpass.getpass('DSS key password: ')
#            key = paramiko.DSSKey.from_private_key_file(path, password)
#        t.auth_publickey(username, key)
#    else:
#        pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
#        t.auth_password(username, pw)

    default_path = os.path.join(os.environ['HOME'],'.ssh', 'id_rsa')
   # path = raw_input('RSA key [%s]: ' % default_path)
   # if len(path) == 0:
   #   path = default_path
    try:
      try:
        key = paramiko.RSAKey.from_private_key_file(default_path)
      except paramiko.PasswordRequiredException:
        password = getpass.getpass('RSA key password: ')
        key = paramiko.RSAKey.from_private_key_file(path, password)
      t.auth_publickey(username,key)
    except Exception, e:
      pass


def get_serlst(ops_user):

  try:
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "123456", db = "opdb")
    cursor = conn.cursor ()
    cmd = '''SELECT * FROM userinfo where username = "%s"''' % ops_user
    cursor.execute (cmd)
    rows = cursor.fetchall()
    lst = []
    for row in rows:
       lst.append(row[2])
    return lst

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



# setup logging
paramiko.util.log_to_file('/var/log/rssh.log')

#frank add
ops_user = getpass.getuser()
username = ''
if len(sys.argv) > 1:
    hostname = sys.argv[1]
    if hostname.find('@') >= 0:
        username, hostname = hostname.split('@')
    if (len(username) == 0 or len(hostname) == 0):
      print '''
Usage:
	rssh user@x.x.x.x
	'''
      sys.exit(1)
    
else:
   # hostname = raw_input('Hostname: ')
   print '''
Usage: 
        rssh user@x.x.x.x
	'''
   sys.exit(1)
if len(hostname) == 0:
    print '*** Hostname required.'
    sys.exit(1)
port = 22
if hostname.find(':') >= 0:
    hostname, portstr = hostname.split(':')
    port = int(portstr)
ownlst = get_serlst(ops_user)
print ownlst
if hostname not in ownlst:
  print "Sorry you don't have permission connecting  to %s" % hostname
  sys.exit(1)

# now connect
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
except Exception, e:
    print '*** Connect failed: ' + str(e)
    traceback.print_exc()
    sys.exit(1)

try:
    t = paramiko.Transport(sock)
    try:
        t.start_client()
    except paramiko.SSHException:
        print '*** SSH negotiation failed.'
        sys.exit(1)

    try:
        keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except IOError:
        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
        except IOError:
            print '*** Unable to open host keys file'
            keys = {}

    # check server's host key -- this is important.
    key = t.get_remote_server_key()
    if not keys.has_key(hostname):
        print '*** WARNING: Unknown host key! '
    elif not keys[hostname].has_key(key.get_name()):
        print '*** WARNING: Unknown host key!'
    elif keys[hostname][key.get_name()] != key:
        print '*** WARNING: Host key has changed!!!'
        sys.exit(1)
    else:
        print '*** Host key OK.'
        print ' '

    # get username
    if username == '':
        default_username = getpass.getuser()
        username = raw_input('Username [%s]: ' % default_username)
        if len(username) == 0:
            username = default_username

    agent_auth(t, username)
    if not t.is_authenticated():
        manual_auth(username, hostname)
    if not t.is_authenticated():
        print '*** Authentication failed.'
        t.close()
        sys.exit(1)

    chan = t.open_session()
    chan.get_pty()
    chan.invoke_shell()
    print '*** Here we go!'
    print
    interactive.interactive_shell(chan,hostname,username,ops_user)
    chan.close()
    t.close()

except Exception, e:
    print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)


