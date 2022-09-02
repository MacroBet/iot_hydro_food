
import sys
import threading
from time import sleep



def loop() :
  while(1):
    print("1")
    sleep(2)


if __name__ == "__main__":
   
    t = threading.Event()
    thread = threading.Thread(target=loop, kwargs={})
    thread.start()

    sleep(8)
    
    sys.exit()