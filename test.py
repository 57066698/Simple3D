## expNet npz
from simple3D import Window
from simple3D.components.keyboardRotate import KeyboardRotate
from examples.draw_line import get_axis
import numpy as np

window = Window()
axis = get_axis()
key = KeyboardRotate(window)
key.add(axis)
window.add(key, axis)

window.render()

