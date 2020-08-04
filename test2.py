import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from PIL import Image
import pygame
from pygame.locals import *
import time


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    #        positions         colors          texture coords
    vertices = [-0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0]

    # convert to 32bit float

    vertices = np.array(vertices, dtype=np.float32)

    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               8, 9, 10, 10, 11, 8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = np.array(indices, dtype=np.uint32)

    VERTEX_SHADER = """

              #version 330

              layout(location = 0) in vec3 a_position;
              layout(location = 1) in vec2 a_texture;

              uniform mat4 model; // combined translation and rotation
              uniform mat4 projection; 

              out vec3 v_color;
              out vec2 v_texture;

              void main() {

               gl_Position = projection * model * vec4(a_position, 1.0f);
               v_texture = a_texture;
               
              }
          """

    FRAGMENT_SHADER = """
           #version 330

            in vec2 v_texture;

            out vec4 outColor;
            
            uniform sampler2D s_texture;

           void main() {
              outColor = texture(s_texture, v_texture);
           }

       """

    # Compile The Program and shaders

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))

    # vertex buffer object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # element buffer object
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))
    # uvs
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

    # Texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("test.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glEnable(GL_TEXTURE_2D)

    glUseProgram(shader)

    glClearColor(0.0, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, display[0]/display[1], 0.1, 100)
    translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -10]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * time.time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time.time())
        rotation = pyrr.matrix44.multiply(rot_x, rot_y)
        model = pyrr.matrix44.multiply(rotation, translation)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # Draw Cube
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        pygame.display.flip()
        pygame.time.wait(10)

    glfw.terminate()


if __name__ == "__main__":
    main()
