import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
from simple3D import Mesh, Material
import pyrr
import time
import glfw
from PIL import Image
import cv2

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
uniform mat4 model;
uniform mat4 projection;
out vec3 v_color;
out vec2 v_texture;
void main()
{
    gl_Position = projection * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


class TextureMaterial(Material):
    def __init__(self, texture_np):
        self.texture_np = cv2.cvtColor(texture_np, cv2.COLOR_RGB2RGBA)
        self.VOA = None

    def show_mesh(self, mesh:Mesh):
        self.mesh = mesh
        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                     compileShader(fragment_src, GL_FRAGMENT_SHADER))

        vertices = self.combine_vertices([mesh.vertices, mesh.uvs], [3, 2])
        indices = mesh.indices
        texture = self.texture_np

        if self.VOA is None:
            self.VOA = glGenVertexArrays(1)
        glBindVertexArray(self.VOA)

        # Vertex Buffer Object
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # VAO
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

        gl_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, gl_texture)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture.shape[1], texture.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     texture)

        glUseProgram(self.shader)

        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")

    def render(self, projection, cameraLoc, meshLoc):
        glUseProgram(self.shader)
        glBindVertexArray(self.VOA)
        model = pyrr.matrix44.multiply(meshLoc, cameraLoc)

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_TRIANGLES, len(self.mesh.indices), GL_UNSIGNED_INT, None)