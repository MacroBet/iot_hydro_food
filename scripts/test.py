
from itertools import count
import sys
import threading
from time import sleep



def loop() :
  while(1):
    print("1")
    sleep(2)


if __name__ == "__main__":
   
    # t = threading.Event()
    # thread = threading.Thread(target=loop, kwargs={})
    # thread.start()
    while(1):
      print("1")
      sleep(1)
      count += count
      if count == 3:
    
        sys.exit()