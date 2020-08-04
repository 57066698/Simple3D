from simple3D.tools import ModelLoader
from simple3D import display, MeshObject, Mesh
from simple3D.mats import TextureMaterial
from simple3D.tools import Loader
import numpy as np

npz_path = "C:/Users/User1/Desktop/faceProject/datas/ysx_npz/00001_0.npz"

loader = ModelLoader()
loader.load_npz(npz_path, scale=0.01, trans=(-96, -96, 0))

mesh = Mesh(loader.vertices, loader.indices, uvs=loader.uvs)
mat = TextureMaterial(loader.texture_np)
meshObj = MeshObject(mesh, mat)
display(meshObj)