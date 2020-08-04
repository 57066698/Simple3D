"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import display
from simple3D import Mesh, Scene
from simple3D import MeshObject, MeshObject_muti
from simple3D.mats import TextureMaterial, VectexcolorMaterial
from simple3D.tools.Loader import ModelLoader
import numpy as np
import os

meshs = []
mats = []

dir = "../../datas/exp1_npz/"
npz_filenames = os.listdir(dir)
# subdirs = [f.path for f in os.scandir(dir) if f.is_dir()]

for name in npz_filenames:
    Loader = ModelLoader()
    Loader.load_npz(dir + name, scale=0.2)
    # Loader.load_npz(dir + name, scale=0.01, trans=(-96, -96, 0))
    mesh = Mesh(Loader.vertices, Loader.indices, vectices_color=Loader.vectices_color)
    mat = VectexcolorMaterial()
    meshs.append(mesh)
    mats.append(mat)

meshObj = MeshObject_muti(meshs, mats)
# meshObj.translate(0, 0, 0)
scene = Scene()
scene.add(meshObj)
scene.render()