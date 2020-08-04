"""
    显示一个 x=3, y=2, z=1 的四面体
    @st
"""

from simple3D import display, Scene
from simple3D import Mesh
from simple3D import MeshObject, MeshObject_muti
from simple3D.mats import TextureMaterial, VectexcolorMaterial
from simple3D.tools.Loader import ModelLoader
import numpy as np
import os

meshs = []
mats = []

dir1 = "../../datas/exp1_npz/"
dir2 = "../../datas/exp2_npz/"

def get_sequence_meshObj(dir):
    npz_filenames = os.listdir(dir)

    for name in npz_filenames:
        Loader = ModelLoader()
        Loader.load_npz(dir + name)
        # Loader.load_npz(dir + name, scale=0.01, trans=(-96, -96, 0))
        mesh = Mesh(Loader.vertices, Loader.indices, vectices_color=Loader.vectices_color)
        mat = VectexcolorMaterial()
        meshs.append(mesh)
        mats.append(mat)

    meshObj = MeshObject_muti(meshs, mats)
    return meshObj

face_seq_1 = get_sequence_meshObj(dir1)
face_seq_1.translate(-10, 0, -10)
face_seq_2 = get_sequence_meshObj(dir2)
face_seq_2.translate(10, 0, -10)
scene = Scene()
scene.add(face_seq_1)
scene.add(face_seq_2)
scene.render()
