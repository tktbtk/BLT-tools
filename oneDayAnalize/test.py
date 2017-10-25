from subprocess import Popen
import time

for i in range(5):
    print "thread1"
    p1 = Popen(["python2", "sleep.py"])
    time.sleep(1)
