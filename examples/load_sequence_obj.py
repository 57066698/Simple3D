"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import display
from simple3D import Mesh
from simple3D import MeshObject, MeshObject_muti
from simple3D.mats import TextureMaterial, VectexcolorMaterial
from simple3D.tools.Loader import ModelLoader
import numpy as np
import os

meshs = []
mats = []

dir = "../../datas/expNet_npy1/"
npz_filenames = os.listdir(dir)
# subdirs = [f.path for f in os.scandir(dir) if f.is_dir()]

for i in range(500):
    name = npz_filenames[i]
    Loader = ModelLoader()
    Loader.load_Obj(dir + name, scale=0.1, trans=(0, 0, -4650))
    mesh = Mesh(Loader.vertices, Loader.indices, vectices_color=Loader.vectices_color)
    mat = VectexcolorMaterial()
    meshs.append(mesh)
    mats.append(mat)

meshObj = MeshObject_muti(meshs, mats)
display(meshObj)