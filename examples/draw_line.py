"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import meshObject, material, mesh, display
import numpy as np
from simple3D.mats import vectexcolorMaterial
from simple3D.mats.lineMeterial import LineMeterial

vertices = [0.0, 0.0, 0.0,
            1, 0, 0.0,
            0, 0, 0,
              0, 1, 0,
            0, 0, 0,
            0, 0, 1]

vertices_color = [1, 0, 0,
                  1, 0, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 0, 1,
                  0, 0, 1]

indices = [0, 1, 2, 3, 4, 5]

def get_triangle():
    mesh = mesh(vertices, indices, vectices_color=vertices_color)
    material = LineMeterial()
    meshObj = meshObject(mesh, material)
    return meshObj

if __name__ == "__main__":
    meshObj = get_triangle()
    display(meshObj)