from simple3D.core import displayObject
from simple3D.core.transform import Transfom
import pyrr
import numpy as np

class Camera:
    def __init__(self):
        self.transform = Transfom()
        self.transform.pos = np.array([0, 0, 3])
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        self.dis = 3

    def zoom(self, zoom_num):
        dis = self.transform.pos_length()
        dis = max(dis + zoom_num, 1)
        self.transform.pos = self.transform.pos_normalize() * dis

    def around(self, x, y):
        """
        在球上做对应移动
        :param x:
        :param y:
        """

        # 计算变化值,move 在球面发生的旋转位移

        # 将变化值乘到目标

        # 计算新的pos

        self.transform.pos = self.transform.pos + np.array([-x * 0.01, -y * 0.01, 0])
        self.transform.pos = self.transform.pos_normalize() * self.dis

    def render(self, meshObjs: [displayObject]):
        pos_pyrr = pyrr.matrix44.create_look_at(pyrr.Vector3(self.transform.pos),
                                                pyrr.Vector3([0, 0, 0]),
                                                pyrr.Vector3([0, 1, 0]))

        for meshObject in meshObjs:
            meshObject.render(self.projection, pos_pyrr)