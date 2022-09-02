
import sys
import threading
from time import sleep



def loop() :
  print("1")
  sleep(5)


if __name__ == "__main__":
   

    thread = threading.Thread(target=loop, kwargs={})
    thread.start()

    sleep(8)
    thread.join()
    sys.exit()