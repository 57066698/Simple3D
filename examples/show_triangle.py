"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import MeshObject, Material, Mesh, display
import numpy as np
from simple3D.mats import VectexcolorMaterial

vertices_and_color = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            1.5, 0, 0.0, 0.0, 1.0, 0.0,
              0, 1, 0.0, 0.0, 0.0, 1.0,
              0, 0, 0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2,
           0, 2, 3,
           0, 3, 1,
           1, 3, 2]

vertices_and_color_np = np.array(vertices_and_color, dtype=np.float32)
indices_np = np.array(indices, dtype=np.uint32)
vertices_np = vertices_and_color_np.reshape((-1, 6))[:, 0:3]
vertices_np = vertices_np.reshape((-1))
color_np = vertices_and_color_np.reshape((-1, 6))[:, 3:]
color_np = color_np.reshape((-1))

def get_triangle():
    mesh = Mesh(vertices_np, indices, vectices_color=color_np)
    material = VectexcolorMaterial()
    meshObj = MeshObject(mesh, material)
    return meshObj

if __name__ == "__main__":
    meshObj = get_triangle()
    display(meshObj)