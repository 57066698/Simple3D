"""
    打开一个窗口，显示其中内容
"""

import glfw
from OpenGL.GL import *
from simple3D import Camera, DisplayObject, Material, Component, ViewPort, Scene
from simple3D.components.mouseRotate import MouseRotate
import threading

class Window:
    def __init__(self, WIDTH=1280, HEIGHT=720, framerate=25, name="Display"):
        self.width = WIDTH
        self.height = HEIGHT
        # initializing glfw library
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        self.window = glfw.create_window(self.width, self.height, name, None, None)
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

        self.scenes = []
        self.viewports = []
        self.cameras = []
        self.update_calls = []
        self.components = []
        self.frame_rate = framerate

        self.thread = None
        self.stop_render = False

    def start(self):
        self.stop_render = False
        self.thread = threading.Thread(target=self.render, args=())
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()

    def stop(self):
        self.stop_render = True

    @property
    def default_camera(self):
        if len(self.cameras) == 0:
            self.camera = Camera(self.width, self.height)
        return self.camera

    @property
    def default_scene(self):
        if len(self.scenes) == 0:
            self.scenes.append(Scene())
        return self.scenes[0]

    @property
    def default_viewport(self)->ViewPort:
        if len(self.viewports) == 0:
            viewPort = ViewPort(0, 0, self.width, self.height, scene=self.default_scene)
            self.viewports.append(viewPort)
        return self.viewports[0]

    def window_resize(self, window, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)

    def splitViewPorts(self, rows, cols):
        viewPorts = ViewPort.get_aranged_viewports(self.width, self.height, rows, cols)
        self.add(*viewPorts)

    def add(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                self.default_viewport.scene.add(item)
            elif callable(item):
                self.update_calls.append(item)
            elif isinstance(item, ViewPort):
                self.viewports.append(item)
                if item._scene and (item._scene not in self.scenes):
                    self.scenes.append(item._scene)
            elif isinstance(item, Scene):
                self.scenes.append(item)
            elif isinstance(item, Component):
                self.components.append(item)
        return self

    def remove(self, *args):
        for item in args:
            if isinstance(item, DisplayObject):
                for scene in self.scenes:
                    scene.remove(item)
            elif isinstance(item, Component):
                self.components.remove(item)
            elif callable(item):
                self.update_calls.remove(item)
            elif isinstance(item, ViewPort):
                self.viewports.remove(item)
            elif isinstance(item, Scene):
                self.scenes.remove(item)

    def update(self):
        for scene in self.scenes:
            scene.update()
        for call in self.update_calls:
            call()
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

    def render_viewport(self, viewport:ViewPort):

        displayObjects = viewport.scene.displayObjs
        if len(displayObjects) == 0: return
        glViewport(viewport.x, viewport.y, viewport.width, viewport.height)
        camera = viewport.camera
        camera_lookat = camera.lookat_matrix
        camera_projection = camera.projection

        for obj in displayObjects:
            if obj.material and isinstance(obj.material, Material):
                if not obj.is_showing:
                    obj.show()
                obj.material.render(camera_projection, camera_lookat, obj.transform.render_matrix)

    def display_cube(self):
        from . import Mesh
        from .mats.vectexcolorMaterial import VectexcolorMaterial
        vertices = [0.0, 0.0, 0.0,
                    1.5, 0, 0.0,
                    0, 1, 0.0,
                    0, 0, 0.5]

        color = [1.0, 0.0, 0.0,
                 0.0, 1.0, 0.0,
                 0.0, 0.0, 1.0,
                 1.0, 1.0, 1.0]

        indices = [0, 1, 2,
                   0, 2, 3,
                   0, 3, 1,
                   1, 3, 2]

        mesh = Mesh(vertices, indices, vectices_color=color)
        material = VectexcolorMaterial()
        meshObj = DisplayObject(mesh, material)
        self.add(meshObj)
        self.render()

def display(*displayObjects, rows = 1, cols = 1, components=None, muti_viewport=True):

    width, height = 1280, 720
    window = Window(width, height)

    if muti_viewport:
        viewPorts = ViewPort.get_aranged_viewports(width, height, rows, cols)
        for i in range(len(displayObjects)):
            scene = Scene()
            scene.add(displayObjects[i])
            window.add(scene)
            viewPorts[i].add(scene)
        window.add(*viewPorts)
    else:
        window.add(*displayObjects)
    mouseMove = MouseRotate(window)
    mouseMove.add(*displayObjects)
    window.add(mouseMove)
    if components:
        window.add(*components)
    window.render()

    return window