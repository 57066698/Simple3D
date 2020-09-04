"""
    openGL 渲染封装
"""

import glfw
from OpenGL.GL import *
from simple3D import Camera, DisplayObject, Material, Component, ViewPort
from simple3D.components.mouseRotate import MouseRotate
import numpy as np

class Scene:
    def __init__(self, WIDTH=1280, HEIGHT=720, framerate=25, use_default_viewport=True):
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

        self.displayObjs = []
        self.components = []
        self.update_calls = []
        self.viewports = []
        self.frame_rate = framerate
        if use_default_viewport:
            self.viewports.append(ViewPort(0, 0, self.width, self.height
                                           , render_scene=True, use_default_camera=True))

        self.camera = None

    @property
    def default_camera(self):
        if self.camera == None:
            self.camera = Camera(self.width, self.height)
        return self.camera

    def window_resize(self, window, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.append(item)
            elif isinstance(item, Component):
                self.components.append(item)
            elif callable(item):
                self.update_calls.append(item)
            elif isinstance(item, ViewPort):
                self.viewports.append(item)

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.displayObjs.remove(item)
            elif isinstance(item, Component):
                self.components.remove(item)
            elif callable(item):
                self.update_calls.remove(item)
            elif isinstance(item, ViewPort):
                self.viewports.append(item)

    def update(self):
        for component in self.components:
            component.update()
        for call in self.update_calls:
            call()

    def render_scene(self):

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
                # events
                self.update()
                # clear buffer
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                # render viewports
                for viewport in self.viewports:
                    self.render_viewport(viewport)
                # show buffer to scene
                glfw.swap_buffers(self.window)
                previous = previous + time

        glfw.terminate()

    def render_viewport(self, viewport):

        displayObjects = viewport.displayObjs + self.displayObjs if viewport.render_scene \
            else viewport.displayObjs
        if len(displayObjects) == 0: return

        glViewport(viewport.x, viewport.y, viewport.width, viewport.height)
        camera = self.default_camera if viewport.use_default_camera else viewport.camera
        camera_lookat = camera.lookat_matrix
        camera_projection = camera.projection

        for obj in displayObjects:
            if obj.material and isinstance(obj.material, Material):
                if not obj.is_showing:
                    obj.show()
                obj.material.render(camera_projection, camera_lookat, obj.transform.render_matrix)


def display(*displayObjects, rows = 1, cols = 1, components=None, muti_viewport=True, mouseRotae=True):

    width, height = 1280, 720
    scene = Scene(width, height, use_default_viewport=not muti_viewport)

    if muti_viewport:
        viewPorts = ViewPort.get_aranged_viewports(width, height, rows, cols)
        for i in range(len(displayObjects)):
            viewPorts[i].add(displayObjects[i])
        scene.add(*viewPorts)
    else:
        scene.add(*displayObjects)
    mouseMove = MouseRotate(scene)
    mouseMove.add(*displayObjects)
    scene.add(mouseMove)
    if components:
        scene.add(*components)
    scene.render_scene()

    return scene