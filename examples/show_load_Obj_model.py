from simple3D.tools import ModelLoader
from simple3D import display, MeshObject, Mesh
from simple3D.mats import TextureMaterial, VectexcolorMaterial

obj_path = "../../datas/111/subject0.obj"

loader = ModelLoader()
loader.load_Obj(obj_path, scale=0.01, trans=(0, 0, -4650))

print(loader)

mesh = Mesh(loader.vertices, loader.indices, vectices_color=loader.vectices_color)
mat = VectexcolorMaterial()
meshObj = MeshObject(mesh, mat)
display(meshObj)