#!/usr/bin/env python
#coding:utf-8
import requests
import time
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def check_url():
  f = file('./s.txt','r')
  for line in f.readlines():
    try:
      result = requests.get('http://'+line.strip()).text
      if "沪ICP备" in result:
        print line.strip(),'is OK.'
      else:
        print line.strip(),'is not Ok.'
    except Exception as e:
      print e
      pass
  f.close()
def ttt():
  for i in range(5):
    print '++++++++++++',  i
    time.sleep(0.1)
  

p1 = threading.Thread(target=check_url)
p2 = threading.Thread(target=ttt)
if __name__ == '__main__':
  p1.start()
  p2.start()
  
#i = 0
#while True:
#  r = requests.get('http://oneokrock.fjtj8.com')
#  print r.text
#  print i
#  i += 1
#  time.sleep(1)

