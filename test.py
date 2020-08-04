## expNet npz

import numpy as np
import os

data = np.load("../datas/output_tar_npz/subject000.npz")

vertices = data['v']
vertices = vertices.reshape((-1, 3))

x_range = (np.min(vertices[:, 0]), np.max(vertices[:, 0]))
y_range = (np.min(vertices[:, 1]), np.max(vertices[:, 1]))
z_range = (np.min(vertices[:, 2]), np.max(vertices[:, 2]))

print(x_range, y_range, z_range)