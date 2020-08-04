import numpy as np
import os
from simple3D.tools import ModelLoader

dir = '../datas/expNet_npy1/'

obj_filenames = os.listdir(dir)

# 全部按第一个调整尺寸
Loader = ModelLoader()
Loader.load_Obj(dir + obj_filenames[0], scale=0.01, trans=(0, 0, -4650))





for filename in obj_filenames:
    Loader = ModelLoader()
    Loader.load_Obj(in_dir + filename, scale=0.01, trans=(0, 0, -4650))

    Loader.save_npz(out_dir + filename[:-4])