## expNet npz
import pyrr
import numpy as np
from simple3D import Transform

trans = Transform()
trans.euler = [np.pi/2, 0, 0]

P = [1, 1, 1]

print(np.dot(trans.rotation, P))
print(np.dot(P, trans.rotation))