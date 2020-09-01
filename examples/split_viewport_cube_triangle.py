from examples.show_cube_with_texture import get_cube
from examples.show_triangle import get_triangle

from simple3D.components.mouseRotate import MouseRotate
from simple3D import Scene, ViewPort, display

if __name__ == "__main__":
    cube = get_cube()
    triangle = get_triangle()

    display(cube, triangle, rows=1, cols=2)
