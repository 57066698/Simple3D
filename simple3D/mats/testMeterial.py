import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
from simple3D import mesh, material
import pyrr
import time
import glfw


vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
layout(location = 2) in vec3 a_position2;
uniform mat4 model;
uniform mat4 projection;
out vec3 v_color;
void main()
{
    gl_Position = projection * model * vec4((a_position+a_position2), 1.0);
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

class TestMeterial(material):
    def __init__(self):
        self.mesh = None
        self.VOA = None
        self.VOB = None
        self.count = 0

    def show_mesh(self, mesh:mesh):
        self.mesh = mesh

        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                     compileShader(fragment_src, GL_FRAGMENT_SHADER))

        pos2 = np.zeros_like(self.mesh.indices, dtype=np.float32)
        pos2 = np.reshape(pos2, (-1, 3))
        pos2[:, 2] = 0
        pos2 = np.reshape(pos2, (-1))

        if self.VOA is None:
            self.VOA = glGenVertexArrays(1)
        glBindVertexArray(self.VOA)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBufferData(GL_ARRAY_BUFFER, mesh.vertices.nbytes+mesh.vertices_color.nbytes+pos2.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, None, self.mesh.vertices)
        glBufferSubData(GL_ARRAY_BUFFER, mesh.vertices.nbytes, None, mesh.vertices_color)
        glBufferSubData(GL_ARRAY_BUFFER, mesh.vertices.nbytes + mesh.vertices_color.nbytes, None, pos2)

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.indices.nbytes, mesh.indices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(48))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(96))

        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")

    def render(self, projection, cameraLoc, meshLoc):
        glUseProgram(self.shader)
        glBindVertexArray(self.VOA)

        pos2 = np.zeros_like(self.mesh.indices, dtype=np.float32)
        pos2 = np.reshape(pos2, (-1, 3))
        pos2[:, 2] = 0.01 * self.count
        pos2 = np.reshape(pos2, (-1))
        self.count = self.count + 1

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferSubData(GL_ARRAY_BUFFER, self.mesh.vertices.nbytes+self.mesh.vertices_color.nbytes, pos2.nbytes, pos2)

        model = pyrr.matrix44.multiply(meshLoc, cameraLoc)

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_TRIANGLES, len(self.mesh.indices), GL_UNSIGNED_INT, None)