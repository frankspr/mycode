import time
import threading

number = 0

lock = threading.RLock()

def run(num):
  lock.acquire()
  global number
  number += 1
  print number
  lock.release()
  time.sleep(2)

for i in range(20):
  t = threading.Thread(target=run,args=(i,))
  t.start()
