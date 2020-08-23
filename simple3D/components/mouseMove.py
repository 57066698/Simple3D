"""
    控制多个物体旋转
"""

import glfw
from simple3D import Component

class MouseMove(Component):
    def __init__(self, scene):
        super().__init__()

        glfw.set_mouse_button_callback(scene.window, self.mouse_down_callback)
        glfw.set_scroll_callback(scene.window, self.scroll_callback)
        glfw.set_cursor_pos_callback(scene.window, self.mouse_move_callback)

        # mouse
        self.lastX, self.lastY = scene.width / 2, scene.height / 2
        self.first_mouse = True
        self.is_mouse_left_down = False
        self.cached_mouse_move_X = 0
        self.cached_mouse_move_Y = 0
        self.cached_scroll_num = 0
        self.camera = None

    def set_camera(self, camera):
        self.camera = camera

    def update(self):
        # rotate
        self.camera.around(self.cached_mouse_move_X, self.cached_mouse_move_Y)
        self.cached_mouse_move_X = 0
        self.cached_mouse_move_Y = 0
        # zoom
        self.camera.zoom(self.cached_scroll_num)
        self.cached_scroll_num = 0

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

    # 鼠标滚轮
    def scroll_callback(self, window, xoffset, yoffset):
        self.cached_scroll_num = self.cached_scroll_num + yoffset
