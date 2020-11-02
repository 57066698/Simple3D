import threading
from threading import *

import glfw
from threading import *
import time

# 看是否会自动加入

class AA:
    def __init__(self):
        self.thread_stop = False
        self.thread = None

    def run(self):
        while not self.thread_stop:
            print("run", self.thread_stop)
            time.sleep(1)

    def start(self):
        self.thread = threading.Thread(target=self.run, args={})
        self.thread.start()
        print("111")

    def stop(self):
        self.thread_stop = True
        # self.thread.join()

aa = AA()
aa.start()
time.sleep(3)
aa.stop()
time.sleep(3)
print(aa.thread)
