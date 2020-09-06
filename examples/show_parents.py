"""
    two cube
    second is on left-top-front-corner of first
    and 1/4 size
"""

from examples.draw_line import get_axis
from examples.show_triangle import get_triangle

from simple3D.components.mouseRotate import MouseRotate
from simple3D import Window, ViewPort, display
from simple3D.components.mouseRotate import MouseRotate

if __name__ == "__main__":
    axis1 = get_axis()
    axis2 = get_axis()
    axis2.transform.parent = axis1.transform
    axis2.transform.pos = [0, 1, 0]

    window = Window()
    window.add(axis1, axis2)
    mouseRotate = MouseRotate(window)
    mouseRotate.add(axis1)

    window.add(mouseRotate)
    window.render_scene()