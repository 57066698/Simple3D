"""
    openGL 渲染封装
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import numpy as np
import ctypes
from simple3D import mesh, meshObject
from simple3D.Camera import Camera
from simple3D.tools.ScreenShot import screen_shot


class Scene:
    def __init__(self, WIDTH=1280, HEIGHT=720, framerate=25):
        self.width = WIDTH
        self.height = HEIGHT
        # initializing glfw library
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        self.window = glfw.create_window(self.width, self.height, "Display", None, None)
        # check if window was created
        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # mouse
        self.lastX, self.lastY = self.width / 2, self.height / 2
        self.first_mouse = True
        self.is_mouse_left_down = False
        self.cached_mouse_move_X = 0
        self.cached_mouse_move_Y = 0
        self.cached_scroll_num = 0

        self.meshObjs = []
        self.frame_rate = framerate
        # set window's position
        glfw.set_window_pos(self.window, 400, 200)
        # set the callback function for window resize
        glfw.set_window_size_callback(self.window, self.window_resize)
        # make the context current
        glfw.make_context_current(self.window)

        glfw.set_mouse_button_callback(self.window, self.mouse_down_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_move_callback)

        self.camera = None

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)

    # 鼠标左键按下
    def mouse_down_callback(self, window, button, action, mods):
        if button == 0:
            self.is_mouse_left_down = bool(action)
            if action == 0:
                self.first_mouse = True

    # 鼠标移动
    def mouse_move_callback(self, window, xpos, ypos):

        if not self.is_mouse_left_down:
            return

        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.first_mouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos
        self.cached_mouse_move_X = xoffset
        self.cached_mouse_move_Y = yoffset

    # 围绕
    def around(self, camera):
        camera.around(self.cached_mouse_move_X, self.cached_mouse_move_Y)
        self.cached_mouse_move_X = 0
        self.cached_mouse_move_Y = 0

    # 鼠标滚轮
    def scroll_callback(self, window, xoffset, yoffset):
        self.cached_scroll_num = self.cached_scroll_num + yoffset

    def zoom(self, camera):
        camera.zoom(self.cached_scroll_num)
        self.cached_scroll_num = 0

    def add(self, meshObj):
        self.meshObjs.append(meshObj)

    def remove(self, meshObj):
        self.meshObjs.remove(meshObj)

    def render(self):
        if self.camera is None:
            self.camera = Camera()

        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        time = 1 / self.frame_rate  # 帧每秒
        previous = glfw.get_time()

        # the main application loop
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = glfw.get_time()

            if now - previous >= time:
                self.zoom(self.camera)
                self.around(self.camera)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.camera.render(self.meshObjs)
                # screen_shot(self)
                glfw.swap_buffers(self.window)
                previous = previous + time

        glfw.terminate()

def display(meshObj:meshObject):
    scene = Scene()
    scene.add(meshObj)
    scene.render()



