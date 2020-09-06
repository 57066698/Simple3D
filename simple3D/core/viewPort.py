"""
    a viewport
"""
from simple3D import DisplayObject, Camera, Scene, Component
import numpy as np

class ViewPort:
    def __init__(self, x, y, width, height, scene=None, camera=None):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

        self._scene = scene
        self._camera = camera

    @property
    def scene(self)->Scene:
        if self._scene == None:
            self._scene = Scene()
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    @property
    def camera(self)->Camera:
        if self._camera == None:
            self._camera = Camera(self.width, self.height)
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject) or isinstance(item, Component):
                self.scene.add(item)
            if isinstance(item, Scene):
                self.scene = item

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject) or isinstance(item, Component):
                self.scene.remove(item)

    @classmethod
    def get_aranged_viewports(cls, screen_width, screen_height, rows, cols):
        viewPorts = []

        for i in range(rows * cols):
            r = np.int(i / cols)
            c = i - r * rows
            viewPort = cls(x=c * screen_width / cols, y=r * screen_height / rows, width=screen_width / cols, height=screen_height / rows)
            viewPorts.append(viewPort)

        return viewPorts