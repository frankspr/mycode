#!/usr/bin/env python
import requests
import time
i = 0
while True:
  r = requests.get('http://oneokrock.fjtj8.com')
  print r.text
  print i
  i += 1
  time.sleep(1)

