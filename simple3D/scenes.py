"""
    openGL 渲染封装
"""

import glfw
from OpenGL.GL import *
from simple3D import Camera, DisplayObject
from simple3D import Component
from simple3D.components.mouseMove import MouseMove

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
        self.update_calls = []
        self.frame_rate = framerate

        self.camera = None

    @property
    def default_camera(self):
        if self.camera == None:
            self.camera = Camera()
        return self.camera

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.meshObjs.append(item)
            elif isinstance(item, Component):
                self.components.append(item)
            elif callable(item):
                self.update_calls.append(item)

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.meshObjs.remove(item)
            elif isinstance(item, Component):
                self.components.remove(item)
            elif callable(item):
                self.update_calls.remove(item)

    def update(self):
        for component in self.components:
            component.update()
        for call in self.update_calls:
            call()

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
                self.update()
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
    mouseMove = MouseMove(scene)
    mouseMove.set_camera(camera)
    scene.add(mouseMove)
    scene.render()
