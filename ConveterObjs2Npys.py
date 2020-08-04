import numpy as np
import os
import pathlib
from simple3D.tools import ModelLoader

in_dir = "../datas/exp2/"
out_dir = '../datas/exp2_npz/'

pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

obj_filenames = os.listdir(in_dir)

for filename in obj_filenames:
    Loader = ModelLoader()
    Loader.load_Obj(in_dir + filename, scale=0.1)

    Loader.save_npz(out_dir + filename[:-4])