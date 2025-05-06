from scipy.io import loadmat
import numpy as np


filename = r'C:\Users\Administrator\Desktop\8c8c2edb-5d2d-43fd-b2dd-0a53d7f3bbd6\eeg.mat'
data = loadmat(filename)

print(data['EEG']['nbchan'][0][0][0][0])
print(data['EEG']['trials'][0][0][0][0])
print(data['EEG']['pnts'][0][0][0][0])
print(data['EEG']['srate'][0][0][0][0])
# print(data['EEG']['data'])
print(data['EEG']['data'][0][0].shape)
print(data['EEG']['event'][0][0][0][0])
one_data = data['EEG']['event'][0][0][0][0]

datalist = []
print(int(one_data[0]))

for i in range(len(data['EEG']['event'][0][0][0])):
    datalist.append(int(data['EEG']['event'][0][0][0][i][0]))

print(datalist)