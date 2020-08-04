import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
from simple3D import Mesh
import pyrr
import time
import glfw

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
uniform mat4 rotation;
out vec3 v_color;
void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 330
in vec3 v_color;
out vec4 out_color;
void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

class Material:
    def __init__(self):
        raise NotImplemented("error")

    def combine_vertices(self, vertices_list, length_list):
        vertices_2dlist = []
        for i in range(len(vertices_list)):
            vertices_2dlist.append(vertices_list[i].reshape((-1, length_list[i])))
        result = np.concatenate(vertices_2dlist, axis=-1)
        return result

    def show_mesh(self, mesh: Mesh):
        raise NotImplemented("error")

    def render(self, projection, cameraLoc, meshLoc):
        raise NotImplemented("error")