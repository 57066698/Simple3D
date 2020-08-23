"""
    有网格可显示的物体
    @st
"""
import pyrr
from simple3D.core.transform import Transfom

class DisplayObject:
    def __init__(self, mesh, material):
        self.mesh = mesh
        self.material = material
        self._is_showing = False
        self.transfrom = Transfom()

    def render(self, projection, cameraLoc):

        # rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        #
        # meshLoc = pyrr.matrix44.multiply(rot_x, rot_y)

        if not self._is_showing:
            self.material.show_mesh(self.mesh)
            self._is_showing = True
        self.material.render(projection, cameraLoc, pyrr.matrix44.create_from_translation(self.transfrom.pos))
