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
        mat = self.matrix44
        angle_x = np.arctan2(mat[2, 1], mat[2, 2])
        angle_y = np.arctan2(-mat[2, 0], np.sqrt(np.square(mat[2, 1]) + np.square(mat[2, 2])))
        angle_z = np.arctan2(mat[1, 0], mat[0, 0])
        return (angle_x, angle_y, angle_z)

    @euler.setter
    def euler(self, euler_angle):
        euler_matrix44 = pyrr.matrix44.create_from_eulers(euler_angle)
        self.matrix44[:3, :3] = euler_matrix44[:3, :3]