from simple3D import MeshObject, Material, Mesh, display, Scene
import numpy as np
from simple3D.mats import VectexcolorMaterial
from simple3D.mats import TextureMaterial
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from show_triangle import get_triangle
from show_cube_with_texture import get_cube

triangle = get_triangle()
cube = get_cube()
triangle.translate(1, 0, 0)
cube.translate(-1, 0, 0)

scene = Scene()
scene.add(triangle)
scene.add(cube)
scene.render()

