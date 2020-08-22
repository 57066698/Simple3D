"""
    有网格可显示的物体
    @st
"""
import pyrr
import glfw

class MeshObject:
    def __init__(self, mesh, material):
        self.mesh = mesh
        self.material = material
        self._is_showing = False
        self.mesh_loc = pyrr.Matrix44.from_translation(pyrr.Vector3([0, 0, 0]))

    def translate(self, x, y, z):
        self.mesh_loc = self.mesh_loc + pyrr.Matrix44.from_translation(pyrr.Vector3([x, y, z]))

    def render(self, projection, cameraLoc):

        # rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        #
        # meshLoc = pyrr.matrix44.multiply(rot_x, rot_y)

        if not self._is_showing:
            self.material.show_mesh(self.mesh)
            self._is_showing = True
        self.material.render(projection, cameraLoc, self.mesh_loc)
