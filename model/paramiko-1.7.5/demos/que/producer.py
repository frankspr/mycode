import threading,time
import Queue
import random

q = Queue.Queue()

def Produc(name):
  for i in range(20):
    q.put(i)
    print "%s has make %s" % (name,i)
    time.sleep(random.randrange(4))
def Consumer(name):
  count = 0
  while count < 20:
    data = q.get()
    print "%s has get %s" % (name,data)
    count += 1
    time.sleep(random.randrange(2))

p = threading.Thread(target=Produc,args=('frank',))
c = threading.Thread(target=Consumer,args=('spring',))
p.start()
c.start()

