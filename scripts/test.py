
from itertools import count
import sys
import os
import threading
from time import sleep



def loop() :
  while(1):
    print("1")
    sleep(2)


if __name__ == "__main__":
    count = 0
    t = threading.Event()
    thread = threading.Thread(target=loop, kwargs={})
    thread.start()
   
    sleep(6)
    os._exit(0)