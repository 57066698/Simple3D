"""
    有网格可显示的物体
    @st
"""
import pyrr
from simple3D.core.transform import Transform

class DisplayObject:
    def __init__(self, mesh, material):
        self.mesh = mesh
        self.material = material
        self._is_showing = False
        self.transform = Transform()

    @property
    def is_showing(self):
        return self._is_showing

    def show(self):
        self.material.show_mesh(self.mesh)
        self._is_showing = True

    def render(self, projection, cameraLoc):
        self.material.render(projection, cameraLoc, self.transform.render_matrix)
