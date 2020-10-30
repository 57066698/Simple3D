import threading
from threading import *

import glfw
from threading import *
print(current_thread().getName())
def mt():
    from simple3D import Window

    window = Window()
    window.display_cube()
    print(current_thread().getName())

child=Thread(target=mt)
child.start()
print("Executing thread name :",current_thread().getName())