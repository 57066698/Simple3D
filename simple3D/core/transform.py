"""
    控制位置缩放信息
"""
import pyrr
import numpy as np

class Transform:
    def __init__(self):
        self.matrix44 = pyrr.matrix44.create_identity()

    """
        ---------------------   translates   --------------------
    """
    @property
    def pos(self):
        return self.matrix44[3, :-1]

    @pos.setter
    def pos(self, value):
        self.matrix44[3, :-1] = value

    def translate(self, x, y, z):
        self.matrix44[3, :-1] += np.array([x, y, z])

    def pos_length(self):
        return np.linalg.norm(self.pos)

    def pos_normalize(self):
        return self.pos / self.pos_length()

    """
        ------------------------   rotations   ----------------
    """

    def rotate(self, matrix44):
        self.matrix44[:3, :3] = np.dot(self.matrix44[:3, :3], matrix44[:3, :3])

    @property
    def euler(self):
        RM = self.matrix44
        angle_x = np.arctan2(RM[2, 1], RM[2, 2])
        angle_y = np.arctan2(-RM[2, 0], np.sqrt(np.square(RM[2, 1]) + np.square(RM[2, 2])))
        angle_z = np.arctan2(RM[1, 0], RM[0, 0])
        return (angle_x, angle_y, angle_z)

    @euler.setter
    def euler(self, euler_angle):
        self.matrix44[:3, :3] = euler2RM(euler_angle)

    @property
    def rotation(self):
        return self.matrix44[:3, :3]

    @rotation.setter
    def rotation(self, mat33):
        self.matrix44[:3, :3] = mat33

    def transform_point(self, point):
        point = np.concatenate((point, [1]), axis=0)
        return np.dot(point, self.matrix44)[:3]


def euler2RM(euler):
    """

    :param euler:
    :return:
    """
    sinP, cosP = np.sin(euler[0]), np.cos(euler[0])
    sinTheta, cosTheta = np.sin(euler[1]), np.cos(euler[1])
    sinC, cosC = np.sin(euler[2]), np.cos(euler[2])

    rm_x = np.array([1, 0, 0, 0, cosP, -sinP, 0, sinP, cosP]).reshape((3, 3))
    rm_y = np.array([cosTheta, 0, sinTheta, 0, 1, 0, -sinTheta, 0, cosTheta]).reshape((3, 3))
    rm_z = np.array([cosC, -sinC, 0, sinC, cosC, 0, 0, 0, 1]).reshape((3, 3))

    rm_zyx = np.dot(np.dot(rm_z, rm_y), rm_x)

    return rm_zyx