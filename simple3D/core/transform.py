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
        self.matrix44 = np.dot(self.matrix44, matrix44)