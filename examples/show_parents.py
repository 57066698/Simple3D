"""
    two cube
    second is on left-top-front-corner of first
    and 1/4 size
"""

from examples.show_cube_with_texture import get_cube
from examples.show_triangle import get_triangle

from simple3D.components.mouseRotate import MouseRotate
from simple3D import Scene, ViewPort, display

if __name__ == "__main__":
    cube1 = get_cube()
    cube2 = get_cube()
    cube2.transform.parent = cube1.transform
    cube2.transform.pos = [-1, 1, 1]

    display(cube1, cube2, rows=1, cols=2, muti_viewport=False)