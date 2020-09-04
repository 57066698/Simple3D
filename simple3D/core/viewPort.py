"""
    a viewport
"""
from simple3D import DisplayObject, Camera
import numpy as np

class ViewPort:
    def __init__(self, x, y, width, height, render_scene=False, use_default_camera=False):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.render_scene = render_scene
        self.use_default_camera = use_default_camera

        self.camera = None if use_default_camera else Camera(width, height)
        self.displayObjs = []

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.append(item)

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.append(item)

    @classmethod
    def get_aranged_viewports(cls, screen_width, screen_height, rows, cols):
        viewPorts = []

        for i in range(rows * cols):
            r = np.int(i / cols)
            c = i - r * rows
            viewPort = cls(x=c * screen_width / cols, y=r * screen_height / rows, width=screen_width / cols, height=screen_height / rows,
                                    use_default_camera=False, render_scene=False)
            viewPorts.append(viewPort)

        return viewPorts