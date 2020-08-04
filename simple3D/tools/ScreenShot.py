import numpy as np
import cv2
from OpenGL.GL import *

count = 1
dir = "../screen_shots/"

def screen_shot(scene):
    global count
    img = glReadPixels(0, 0, scene.width, scene.height, GL_RGB, GL_FLOAT)
    img = img * 255.0
    img = np.array(img, dtype=np.uint8)
    cv2.imwrite(dir+str(count)+".jpg", img)
    count = count + 1