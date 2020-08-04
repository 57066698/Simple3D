"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import display
from simple3D import Mesh
from simple3D import MeshObject, MeshObject_muti
from simple3D.mats import TextureMaterial
import numpy as np

vertices_and_uv = [-0.5, -0.5,  0.5, 0.0, 0.0,
                 0.5, -0.5,  0.5, 1.0, 0.0,
                 0.5,  0.5,  0.5, 1.0, 1.0,
                -0.5,  0.5,  0.5, 0.0, 1.0,

                -0.5, -0.5, -0.5, 0.0, 0.0,
                 0.5, -0.5, -0.5, 1.0, 0.0,
                 0.5,  0.5, -0.5, 1.0, 1.0,
                -0.5,  0.5, -0.5, 0.0, 1.0,

                 0.5, -0.5, -0.5, 0.0, 0.0,
                 0.5,  0.5, -0.5, 1.0, 0.0,
                 0.5,  0.5,  0.5, 1.0, 1.0,
                 0.5, -0.5,  0.5, 0.0, 1.0,

                -0.5,  0.5, -0.5, 0.0, 0.0,
                -0.5, -0.5, -0.5, 1.0, 0.0,
                -0.5, -0.5,  0.5, 1.0, 1.0,
                -0.5,  0.5,  0.5, 0.0, 1.0,

                -0.5, -0.5, -0.5, 0.0, 0.0,
                 0.5, -0.5, -0.5, 1.0, 0.0,
                 0.5, -0.5,  0.5, 1.0, 1.0,
                -0.5, -0.5,  0.5, 0.0, 1.0,

                 0.5, 0.5, -0.5, 0.0, 0.0,
                -0.5, 0.5, -0.5, 1.0, 0.0,
                -0.5, 0.5,  0.5, 1.0, 1.0,
                 0.5, 0.5,  0.5, 0.0, 1.0]

indices = [ 0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9, 10, 10, 11,  8,
           12, 13, 14, 14, 15, 12,
           16, 17, 18, 18, 19, 16,
           20, 21, 22, 22, 23, 20]

vertices_and_uv_np = np.array(vertices_and_uv, dtype=np.float32)
indices_np = np.array(indices, dtype=np.uint32)
vertices_np = vertices_and_uv_np.reshape((-1, 5))[:, 0:3]
vertices_np = vertices_np.reshape((-1))
uv_np = vertices_and_uv_np.reshape((-1, 5))[:, 3:5]
uv_np = uv_np.reshape((-1))

meshs = []
mats = []

for i in range(100):
    mesh = Mesh(np.array(vertices_np), np.array(indices), uvs=np.array(uv_np))
    mat = TextureMaterial(texture_path="resources/box.png")
    meshs.append(mesh)
    mats.append(mat)

meshObj = MeshObject_muti(meshs, mats)
display(meshObj)