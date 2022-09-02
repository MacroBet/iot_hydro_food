
import sys
import threading
from time import sleep



def loop() :
  print("1")
  sleep(2)


if __name__ == "__main__":
   

    thread = threading.Thread(target=loop, kwargs={})
    thread.start()

    sleep(8)
    print("shutdown")
    thread.join()
    sys.exit()