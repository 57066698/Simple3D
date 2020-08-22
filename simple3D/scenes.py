"""
    openGL 渲染封装
"""

import glfw
from OpenGL.GL import *
from simple3D import Camera, MouseMove


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

        # make the context current
        glfw.make_context_current(self.window)
        # set window's position
        glfw.set_window_pos(self.window, 400, 200)
        # set the callback function for window resize
        glfw.set_window_size_callback(self.window, self.window_resize)

        self.meshObjs = []
        self.components = []
        self.frame_rate = framerate

        self.camera = None

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)

    def register(self, component):
        self.components.append(component)

    def unregister(self, component):
        self.components.remove(component)

    def add(self, meshObj):
        self.meshObjs.append(meshObj)

    def remove(self, meshObj):
        self.meshObjs.remove(meshObj)

    def update_components(self):
        for component in self.components:
            component.update()

    def render(self):

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
                self.update_components()
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.camera.render(self.meshObjs)
                # screen_shot(self)
                glfw.swap_buffers(self.window)
                previous = previous + time

        glfw.terminate()


def display(meshObj):
    width, height = 1280, 720
    scene = Scene(width, height)
    scene.add(meshObj)
    camera = Camera()
    scene.camera = camera
    mouseMove = MouseMove(scene.window, width, height)
    mouseMove.set_camera(camera)
    scene.register(mouseMove)
    scene.render()
