from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from simple3D import Material, Mesh
import numpy as np
import pyrr

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
uniform mat4 model;
uniform mat4 projection;
out vec3 v_color;
void main()
{
    gl_Position = projection * model * vec4(a_position, 1.0);
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



class LineMeterial(Material):
    def __init__(self):
        super().__init__()

    def show_mesh(self, mesh):
        self.mesh = mesh

        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                     compileShader(fragment_src, GL_FRAGMENT_SHADER))

        vertices_loc = self.mesh.vertices.reshape((-1, 3))
        vertices_color = self.mesh.vertices_color.reshape((-1, 3))
        combined_vertices = np.concatenate((vertices_loc, vertices_color), axis=1).reshape((-1))

        if self.VOA is None:
            self.VOA = glGenVertexArrays(1)
        glBindVertexArray(self.VOA)

        # Vertex Buffer Object
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBufferData(GL_ARRAY_BUFFER, combined_vertices.nbytes, combined_vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.indices.nbytes, mesh.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")


    def render(self, projection, cameraLoc, meshLoc):
        glUseProgram(self.shader)
        glBindVertexArray(self.VOA)
        model = pyrr.matrix44.multiply(meshLoc, cameraLoc)

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_LINES, len(self.mesh.indices), GL_UNSIGNED_INT, None)
