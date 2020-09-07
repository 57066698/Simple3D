"""
    控制多个物体旋转
"""

import glfw
import pyrr
from simple3D import Component, DisplayObject, Transform
from simple3D.core.transform import euler2RM
import numpy as np

class KeyboardMover(Component):
    def __init__(self, scene):
        super().__init__()

        glfw.set_key_callback(scene.window, self.key_callback)
        # key
        self.down_keys = []
        #
        self.transforms = []

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.transforms.append(item.transform)
            elif isinstance(item, Transform):
                self.transforms.append(item)

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.transforms.remove(item.transform)
            elif isinstance(item, Transform):
                self.transforms.remove(item)

    def update(self):
        pass

    def key_callback(self, window, key, scancode, action, mods):

        v = 0.03

        if action in [1, 2]:
            if key == glfw.KEY_W:
                x, y, z = 0, 0, v
            elif key == glfw.KEY_S:
                x, y, z = 0, 0, -v
            elif key == glfw.KEY_A:
                x, y, z = v, .0, 0
            elif key == glfw.KEY_D:
                x, y, z = -v, .0, 0
            elif key == glfw.KEY_E:
                x, y, z = 0, v, 0
            elif key == glfw.KEY_Q:
                x, y, z = 0, -v, 0
            else:
                return

            for obj in self.transforms:
                obj.translate(x, y, z)