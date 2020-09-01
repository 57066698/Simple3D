"""
    a viewport
"""
from simple3D import DisplayObject, Camera

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