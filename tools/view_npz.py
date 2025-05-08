import numpy as np

filename = r"C:\Users\Administrator\Desktop\8c8c2edb-5d2d-43fd-b2dd-0a53d7f3bbd6\save\S1\sample_0.npz"


data = np.load(filename, allow_pickle=True)
print(data['data'].shape)