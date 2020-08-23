## expNet npz
import pyrr
import numpy as np

m1 = pyrr.matrix44.create_from_eulers([0.1, 0, 0])
m2 = pyrr.matrix44.create_from_eulers([0.1, 0, 0])
print(np.dot(m1, m2))