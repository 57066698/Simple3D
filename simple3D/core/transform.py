"""
    控制位置缩放信息
"""

import numpy as np

class Transfom:
    def __init__(self):
        self._pos = np.zeros(3)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def translate(self, x, y, z):
        self._pos += np.array([x, y, z])

    def pos_length(self):
        return np.linalg.norm(self._pos)

    def pos_normalize(self):
        return self._pos / self.pos_length()