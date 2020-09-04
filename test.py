## expNet npz
from simple3D import Transform
import numpy as np

a = Transform()
a.rotate(Transform.euler2RM([0, np.pi/2, 0]))
b = Transform()
b.rotate(Transform.euler2RM([np.pi/2, 0, 0]))

ab = np.dot(a.matrix44, b.matrix44)
ba = np.dot(b.matrix44, a.matrix44)

print(np.dot(ab, [0, 1, 0, 1]))
print(np.dot(ba, [0, 1, 0, 1]))