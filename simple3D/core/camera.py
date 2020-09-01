from simple3D.core import displayObject
from simple3D.core.transform import Transform
import pyrr
import numpy as np

class Camera:
    def __init__(self, width=1280, height=720):
        self.transform = Transform()
        self.transform.pos = np.array([0, 0, 3])
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        self.dis = 3

    def zoom(self, zoom_num):
        dis = self.transform.pos_length()
        dis = max(dis + zoom_num, 1)
        self.transform.pos = self.transform.pos_normalize() * dis
        self.dis = dis

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

    @property
    def lookat_matrix(self):
        return create_look_at(self.transform.pos, np.array([0, 0, 0]), np.array([0, 1, 0]))

    @property
    def projection_matrix(self):
        return self.projection

    # def render(self, meshObjs: [displayObject]):
    #     # pos_pyrr = pyrr.matrix44.create_look_at(pyrr.Vector3(self.transform.pos),
    #     #                                         pyrr.Vector3([0, 0, 0]),
    #     #                                         pyrr.Vector3([0, 1, 0]))
    #
    #     look_at =
    #
    #     for meshObject in meshObjs:
    #         meshObject.render_scene(self.projection, look_at)

def _normalize(vector):
    return vector / np.linalg.norm(vector)

def create_look_at(eye, target, up_vector, dtype=np.float64):
    forward = _normalize(target - eye)
    right = _normalize(np.cross(forward, up_vector))
    up = _normalize(np.cross(right, forward))

    m = np.array(((right[0], up[0], -forward[0], 0.),
                  (right[1], up[1], -forward[1], 0.),
                  (right[2], up[2], -forward[2], 0.),
                  (-np.dot(right, eye), -np.dot(up, eye), np.dot(forward, eye), 1.0)
                  ), dtype=dtype)

    return m