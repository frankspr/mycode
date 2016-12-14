#!/usr/bin/env python
#coding:utf-8
import os
import paramiko
import datetime
import time
import Config 
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

class pushcode():
  '''define push class'''
  def pushjob(self,environ,appname,version):
    self.environ = environ
    self.appname = appname
    self.version = version
    self.ymlpath = str(Config.read_config(basepath+'/conf/config.ini','public','rymlpath'))
    print environ,appname,version
    cmd = '''ansible-playbook %spush.yml -e "environ=%s version=%s name=%s"''' % (self.ymlpath,environ,version,appname)
    print cmd
    self.rcommand(cmd)


  def rollbackapp(self,environ,appname,version):
    self.environ = environ
    self.appname = appname
    self.version = version
    self.ymlpath = str(Config.read_config(basepath+'/conf/config.ini','public','rymlpath'))
    cmd = '''ansible-playbook %srollback.yml -e "environ=%s version=%s name=%s" ''' % (self.ymlpath,environ,version,appname)
    print cmd
    self.rcommand(cmd)
  def rcommand(self,cmd):
    self.pkey = str(Config.read_config(basepath+'/conf/config.ini','public','pkey'))
    self.key = paramiko.RSAKey.from_private_key_file(self.pkey)
    self.ssh = paramiko.SSHClient()
    self.ssh.load_system_host_keys()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if self.environ == 'test':
      self.jumaddr = str(Config.read_config(basepath+'/conf/config.ini','test','jumaddress'))
    if self.environ == 'pre':
      self.jumaddr = str(Config.read_config(basepath+'/conf/config.ini','pre','jumaddress'))
    if self.environ == 'prod':
      self.jumaddr = str(Config.read_config(basepath+'/conf/config.ini','prod','jumaddress'))
    print self.jumaddr
    try:
     # self.ssh.connect(self.jumaddr,22,"username","passwd")
      self.ssh.connect(self.jumaddr,22,"root",pkey=self.key)
      stdin, stdout, stderr = self.ssh.exec_command(cmd)
      aa = stdout.read()
      self.now = str(datetime.datetime.now())
      self.logfile = str(Config.read_config(basepath+'/conf/config.ini','public','logpath'))+"/push"+"-"+str(time.strftime('%Y%m%d'))+".log"
      self.log = open(self.logfile,"a")
      self.log.write(self.now+'\n')
      self.log.write(aa)
      self.log.close()
      self.red_color = '\033[1;31;40m'
      self.green_color = '\033[1;32;40m'
      self.res = '\033[0m'
      print aa
      if "failed=0" in aa:
        print '''%sSuccess !!!%s''' % (self.green_color,self.res)
        print '''%s,%s,%s''' % (self.green_color,aa,self.res)
      else:
        print "push code failed."
        print '''%s,%s,%s''' % (self.red_color,aa,self.res)
      self.ssh.close()
    except Exception,ex:
      print "\n",self.jumaddr,":\t",ex,"\n"
      self.now = str(datetime.datetime.now())
      self.logfile = str(Config.read_config(basepath+'/conf/config.ini','public','logpath'))+"/push_err"+"-"+str(time.strftime('%Y%m%d'))+".log"
      self.log=open(self.logfile,"a")
      self.log.write(self.now+'\n')
      self.log.write("\n"+self.jumaddr+":\t"+str(ex)+"\n")
      self.log.close()
      pass  

    
#c = pushcode()
#c.pushjob(environ='test',appname='website',version='website_201611281433')

