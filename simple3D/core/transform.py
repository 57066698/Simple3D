"""
    控制位置缩放信息
    and parents
"""
import numpy as np

class Transform:
    def __init__(self):
        self.matrix44 = np.identity(4, dtype=np.float64)
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, transform):
        if transform == None:
            self.matrix44 = self.world_matrix44
            self._parent = None
        else:
            self._parent = transform

    @parent.setter
    def parent(self, transform):
        self._parent = transform

    """
        ---------------------   transform    -------------------
    """

    def transform_point(self, point):
        point = np.concatenate((point, [1]), axis=0)
        return np.dot(self.matrix44, point)[:3]

    @property
    def world_matrix44(self):
        if self._parent:
            return np.dot(self._parent.world_matrix44, self.matrix44)
        return self.matrix44

    """
        ---------------------   translates   --------------------
    """
    @property
    def pos(self):
        return self.matrix44[:-1, 3]

    @pos.setter
    def pos(self, value):
        self.matrix44[:-1, 3] = value

    @property
    def world_pos(self):
        return self.world_matrix44[:-1, 3]

    def translate(self, x, y, z):
        self.matrix44[:-1, 3] += np.array([x, y, z])

    def pos_length(self):
        return np.linalg.norm(self.pos)

    def pos_normalize(self):
        return self.pos / self.pos_length()

    """
        ------------------------   rotations   ----------------
    """

    def rotate(self, matrix44):
        self.matrix44[:3, :3] = np.dot(matrix44[:3, :3], self.matrix44[:3, :3])

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

    @property
    def world_rotation(self):
        return self.world_matrix44[:3, :3]

    @property
    def render_matrix(self):
        return np.transpose(self.world_matrix44)

    @classmethod
    def euler2RM(cls, euler):
        sinP, cosP = np.sin(euler[0]), np.cos(euler[0])
        sinTheta, cosTheta = np.sin(euler[1]), np.cos(euler[1])
        sinC, cosC = np.sin(euler[2]), np.cos(euler[2])

        rm_x = np.array([1, 0, 0, 0, cosP, -sinP, 0, sinP, cosP]).reshape((3, 3))
        rm_y = np.array([cosTheta, 0, sinTheta, 0, 1, 0, -sinTheta, 0, cosTheta]).reshape((3, 3))
        rm_z = np.array([cosC, -sinC, 0, sinC, cosC, 0, 0, 0, 1]).reshape((3, 3))

        rm_zyx = np.dot(np.dot(rm_z, rm_y), rm_x)

        return rm_zyx

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