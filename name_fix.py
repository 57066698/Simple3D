import os

dir = "../datas/output_tar_npz/"
npz_filenames = os.listdir(dir)


for name in npz_filenames:
    if len(name) == len("subject0.npz"):
        newName = name.replace("subject", "subject00")
        os.rename(dir+name, dir+newName)

    if len(name) == len("subject10.npz"):
        newName = name.replace("subject", "subject0")
        os.rename(dir + name, dir + newName)