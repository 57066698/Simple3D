"""
    场景，包裹物体, 脚本,
"""

from simple3D import DisplayObject, Component

class Scene:
    def __init__(self):

        self.displayObjs = []
        self.components = []
        self.update_calls = []

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.append(item)
            elif isinstance(item, Component):
                self.components.append(item)
            elif callable(item):
                self.update_calls.append(item)

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.remove(item)
            elif isinstance(item, Component):
                self.components.remove(item)
            elif callable(item):
                self.update_calls.remove(item)

    def update(self):
        for component in self.components:
            component.update()
        for call in self.update_calls:
            call()