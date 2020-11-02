import threading

class AA:
    def __init__(self, name):
        self.name = name

    def call(self):
        print(self.name)
        print(threading.current_thread())

def foo(a):
    a.call()

aa = AA("111")
aa.call()
thread = threading.Thread(target=foo, args={aa})
thread.start()