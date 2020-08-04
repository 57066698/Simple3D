import numpy as np
import os
import cv2
from PIL import Image
"""
    sub module无效
"""


class ModelLoader:
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.uvs = []
        self.vectices_color = []

        self.mat_path = None
        self.sub_mat_name = None
        self.texture_path = None
        self.texture_np = None

    def load_Obj(self, file, scale=1, trans=None):
        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                self.vertices.append(values[1:4])
                if len(values) == 7:
                    self.vectices_color.append(values[4:])
            elif values[0] == 'vt':
                self.uvs.append(values[1:3])
            elif values[0] == 'f':
                for value in values[1:]:
                    val = value.split('/')[0]
                    self.indices.append(int(val)-1)
            elif values[0] == 'mtllib':
                self.mat_path = os.path.dirname(os.path.abspath(file)) + "/" + values[1]
            elif values[0] == 'usemtl':
                self.sub_mat_name = values[1]

        if self.mat_path:
            for line in open(self.mat_path, 'r'):
                if line.startswith('#'): continue
                values = line.split()
                if values[0] == 'map_Kd':
                    self.texture_path = os.path.dirname(os.path.abspath(file)) + "/" + values[1]

        if trans:
            assert len(trans) == 3
            trans = np.array(trans, dtype=np.float32).reshape((1, -1))
            self.vertices = np.array(self.vertices, dtype=np.float32) + trans

        self.vertices = np.array(self.vertices, dtype=np.float32).reshape((-1)) * scale
        self.indices = np.array(self.indices, dtype=np.uint32)
        self.uvs = np.array(self.uvs, dtype=np.float32).reshape((-1))
        if len(self.vectices_color)>0:
            self.vectices_color = np.array(self.vectices_color, dtype=np.float32).reshape((-1))

        # load image to RGBA
        # todo: 考虑原图片 alpha 通道

        if self.texture_path:
            image = cv2.imread(self.texture_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = image[::-1, :, :]  #  opencv 纹理是从下往上 所以上下翻转
            self.texture_np = image.astype(np.uint8)

    def load_npz(self, file, scale=1, trans=None):
        data = np.load(file)

        self.vertices = np.array(data['v'], dtype=np.float32).reshape((-1))
        self.indices = np.array(data['indices'], dtype=np.uint32).reshape((-1))
        if 'vt' in data:
            self.uvs = np.array(data['vt'], dtype=np.float32).reshape((-1))
        if 'texture' in data:
            #  opencv 纹理是从下往上 所以上下翻转
            self.texture_np = np.array(data['texture'], dtype=np.uint8)[::-1, :, :]
        if 'vc' in data:
            self.vectices_color = np.array(data['vc'], dtype=np.float32)

        if trans:
            assert len(trans) == 3
            trans = np.array(trans, dtype=np.float32).reshape((1, -1))
            self.vertices = np.array(self.vertices, dtype=np.float32) + trans

        self.vertices = self.vertices * scale

    def save_npz(self, path):

        if not self.uvs is None:
            np.savez(path, v=self.vertices, indices=self.indices, vt=self.uvs, texture=self.texture_np)

        if not self.vectices_color is None:
            np.savez(path, v=self.vertices, indices=self.indices, vc=self.vectices_color)

        print('saved %s'%path)
