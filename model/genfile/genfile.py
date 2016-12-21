#!/usr/bin/env python
#Frank
serlst='./ser.lst'
fp = open(serlst,'r')
nfp = open('./backend.conf','w')
nfp.write('upstream backend {'+'\n')
nfp.write('	ip_hash;'+'\n')
for ip in fp.readlines():
  print ip.strip()
  nfp.write('	'+'server '+ip.strip()+':8080;'+'\n')
nfp.write('}'+'\n')
fp.close()
nfp.close()


