from simple3D import MeshObject
from OpenGL.GL import *
import pyrr

class Camera:
    def __init__(self):
        self.cameraPos = pyrr.Vector3([0, 0, 3])
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        # self.cameraLoc = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -3]))

    def zoom(self, zoom_num):
        dis = pyrr.vector3.length(self.cameraPos)
        dis = max(dis + zoom_num, 1)
        self.cameraPos = pyrr.vector3.normalise(self.cameraPos) * dis

    def around(self, x, y):
        """
        在球上做对应移动
        :param x:
        :param y:
        """
        dis = pyrr.vector3.length(self.cameraPos)
        self.cameraPos = self.cameraPos + pyrr.Vector3([-x * 0.01, -y * 0.01, 0])
        self.cameraPos = pyrr.vector3.normalise(self.cameraPos) * dis

    def render(self, meshObjs: [MeshObject]):
        self.cameraLoc = pyrr.matrix44.create_look_at(self.cameraPos,
                                                      pyrr.Vector3([0, 0, 0]),
                                                      pyrr.Vector3([0, 1, 0]))

        for meshObject in meshObjs:
            meshObject.render(self.projection, self.cameraLoc)