from simple3D import Transform
from simple3D.core.transform import euler2RM
import numpy as np

euler = [0.1, -0.2, 1.1]
trans = Transform()
trans.translate(0, 0, 0)
trans.euler = euler
p = [1, 1, 1]
p_ = trans.transform_point(p)
euler_x = np.array([1, 0, 0,
                    0, np.cos(euler[0]), -np.sin(euler[0]),
                    0, np.sin(euler[0]), np.cos(euler[0])]).reshape((3, 3))
euler_y = np.array([np.cos(euler[1]), 0, np.sin(euler[1]),
                    0, 1, 0,
                    -np.sin(euler[1]), 0, np.cos(euler[1])]).reshape((3, 3))
euler_z = np.array([np.cos(euler[2]), -np.sin(euler[2]), 0,
                    np.sin(euler[2]), np.cos(euler[2]), 0,
                    0, 0, 1]).reshape((3, 3))

zyx = np.dot(np.dot(euler_z, euler_y), euler_x)

assert np.all(np.equal(p_, np.dot(p, zyx)))
# assert