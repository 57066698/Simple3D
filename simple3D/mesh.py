"""
    物体数据
    @st
"""
import numpy as np

class Mesh:
    def __init__(self, vertices, indices,
                 vectices_color=None,
                 uvs=None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        if not vectices_color is None:
            self.vertices_color = np.array(vectices_color, dtype=np.float32)
        else:
            self.vertices_color = None
        if not uvs is None:
            self.uvs = np.array(uvs, dtype=np.float32)
        else:
            self.uvs = None