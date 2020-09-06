"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import DisplayObject, Mesh, Window
from simple3D.components.mouseRotate import MouseRotate
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
                  1, 1, 1,
                  1, 1, 1]

indices = [0, 1, 2, 3, 4, 5]

def get_axis():
    mesh = Mesh(vertices, indices, vectices_color=vertices_color)
    material = LineMeterial()
    displayObj = DisplayObject(mesh, material)
    return displayObj

if __name__ == "__main__":
    displayObj = get_axis()
    window = Window()
    window.add(displayObj)
    mover = MouseRotate(window)
    mover.add(displayObj)
    window.add(mover)
    window.render_scene()