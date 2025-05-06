import mne


# 读取.set文件
file_path = r'C:\Users\Administrator\Desktop\8c8c2edb-5d2d-43fd-b2dd-0a53d7f3bbd6\2.set'


# 读取分段后的EEGLAB数据
epochs = mne.read_epochs_eeglab(file_path)
print(epochs.info)  # 看看读取结果
print(epochs.info['nchan'])  # 看看读取结果
# eegdata = epochs.get_data()
event = epochs.event_id
#
# print(eegdata)  # (n_epochs, n_channels, n_times)
print(event)

event_ids = epochs.events[:, 2]  # 第三列是事件ID
print(event_ids)

# id_to_label = {v: k for k, v in epochs.event_id.items()}
# print(id_to_label)