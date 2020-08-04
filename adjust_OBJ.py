"""
    移除 vectex color
    vectices z 反向
    添加vt
    f 变为 f/f
"""
import numpy as np

name = "face"
obj_path = "resources/face2.obj"
texture_path = "resources/face2.jpg"
output_dir = "resources/face/"

"""
    分出不同行
"""

v_lines = []
vt_lines = []
other_lines = []
f_lines = []

with open(obj_path, 'r') as f:
    line = f.readline()
    line_index = 0
    while line:
        values = line.split()
        if values[0] == 'v':
            v_lines.append(line)
        elif values[0] == "f":
            f_lines.append(line)
        else:
            other_lines.append(line)

        line_index = line_index + 1
        line = f.readline()

"""
    v 行
    转化为数组 lines, (x, y, z)
    y上翻转
    回归lines
"""
v_data = np.zeros((len(v_lines), 3), dtype=np.float)

for i in range(len(v_lines)):
    values = v_lines[i].split()
    v_data[i, :] = values[1:4]

y_min = np.min(v_data[:, 1])
y_max = np.max(v_data[:, 1])
y_reversed = ((y_max - y_min) - v_data[:, 1]) + y_min
v_data[:, 1] = y_reversed

new_v_lines = []
for i in range(v_data.shape[0]):
    l = v_data[i, :].tolist()
    new_line = "v " + " ".join([str(round(num, 3)) for num in l]) + "\n"
    new_v_lines.append(new_line)

"""
    根据 v_data 取uv
    u = (x-xmin)/(xmax - xmin)
    v = (y-ymin)/(ymax - ymin)
"""
x_min = 1
x_max = 192
y_min = 1
y_max = 192
u = (v_data[:, 0] - x_min) / (x_max - x_min)
v = (v_data[:, 1] - y_min) / (y_max - y_min)

new_vt_lines = []
for i in range(v_data.shape[0]):
    new_vt_lines.append("vt %s %s\n" % (str(round(u[i], 3)), str(round(v[i], 3))))

"""
    所有inds改为 ind/ind 形式
"""
new_f_lines = []
for i in range(len(f_lines)):
    line = f_lines[i]
    values = line.split()
    new_line = "f"
    for j in range(1, len(values), 1):
        num_str = values[j]
        num_str = num_str + "/" + num_str
        new_line = new_line + " " + num_str
    new_line = new_line + "\n"
    new_f_lines.append(new_line)

"""
    添加mtl文件
"""
new_other_lines = []
new_other_lines.append("mtllib %s.mtl\n" % name)
new_other_lines.append("usemtl %s\n" % name)

"""
    写入obj文件
"""
import os

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

line_index = 0
with open(output_dir + name + ".obj", "w") as f:
    f.writelines(new_v_lines)
    f.writelines(new_vt_lines)
    f.writelines(new_other_lines)
    f.writelines(new_f_lines)

"""
    写入mtl, 拷贝Texture
"""
with open(output_dir + name + ".mtl", "w") as f:
    f.write("newmtl %s\n" % name)
    f.write("map_Kd %s\n" % texture_path.split("/")[-1])

from shutil import copyfile

copyfile(texture_path, output_dir + texture_path.split("/")[-1])
