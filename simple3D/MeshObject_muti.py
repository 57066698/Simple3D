"""
    以帧率显示一组网格
    @st
"""
import pyrr

class MeshObject_muti:

    def __init__(self, meshs, materials):
        self.meshs = meshs
        self.materials = materials
        self.count = 0
        self.mesh_loc = pyrr.Matrix44.from_translation(pyrr.Vector3([0, 0, 0]))

    def translate(self, x, y, z):
        self.mesh_loc = self.mesh_loc + pyrr.Matrix44.from_translation(pyrr.Vector3([x, y, z]))

    def render(self, projection, cameraLoc):
        self.materials[self.count].show_mesh(self.meshs[self.count])
        self.materials[self.count].render(projection, cameraLoc, self.mesh_loc)
        self.count = self.count + 1
        if self.count == len(self.materials):
            self.count = 0