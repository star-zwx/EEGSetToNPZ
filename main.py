import glob
import sys
import os
import mne
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from mainWindows import Ui_MainWindow
from scipy.io import loadmat
import numpy as np


class Read_SetData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_data = mne.read_epochs_eeglab(self.file_path)
        if self.file_data:
            self.channel_num = self.file_data.info['nchan']
            self.sfreq = self.file_data.info['sfreq']
            self.trails_num = self.file_data.get_data().shape[0]
            self.sample_num = self.file_data.get_data().shape[2]

        else:
            print("文件读取失败~")

    def get_data(self):
        # (n_epochs, n_channels, n_times)

        return self.file_data.get_data()

    def get_event_dict(self):
        # {'85': 1, '102': 2, '1': 3, '51': 4, '119': 5}
        return self.file_data.event_id

    def get_event_list(self):
        # 按照trials排列的event标签列表，完成映射的
        return self.file_data.events[:, 2]  # 第三列是事件ID


class Read_Mat:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_data = loadmat(self.file_path)
        if self.file_data:
            self.channel_num = self.file_data['EEG']['nbchan'][0][0][0][0]
            self.sfreq = self.file_data['EEG']['srate'][0][0][0][0]
            self.trails_num = self.file_data['EEG']['trials'][0][0][0][0]
            self.sample_num = self.file_data['EEG']['pnts'][0][0][0][0]

        else:
            print("文件读取失败~")

    def get_data(self):
        # (n_epochs, n_times,n_channels)

        return np.transpose(self.file_data['EEG']['data'][0][0], (2, 0, 1))

    def get_event_dict(self):
        eventlist = self.get_event_list()
        mapping = {}
        for idx, value in enumerate(dict.fromkeys(eventlist)):
            mapping[str(value)] = idx + 1

        return mapping

    def get_event_list(self):
        datalist = []
        for i in range(len(self.file_data['EEG']['event'][0][0][0])):
            datalist.append(int(self.file_data['EEG']['event'][0][0][0][i][0]))

        return datalist


class my_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建 UI 对象

        self.ui = Ui_MainWindow()
        # 设置 UI
        self.ui.setupUi(self)
        self.save_path = ''
        self.set_file_onedata = []
        self.set_file_oneevent = []
        self.mat_file_onedata = []
        self.mat_file_oneevent = []
        self.set_file_grpdata = []
        self.set_file_grpevent = []
        self.mat_file_grpdata = []
        self.mat_file_grpevent = []
        self.event_dict = {}
        self.single_group = True  # 控制是否是批处理，True的话，不是批处理

        # 连接槽函数
        self.ui.actionsingle_file.triggered.connect(self.on_ImSetClicked)
        self.ui.actiongroup_files.triggered.connect(self.on_ImSetGrpClicked)
        self.ui.actionsingle_file_2.triggered.connect(self.on_ImMatClicked)
        self.ui.actiongroup_files_2.triggered.connect(self.on_ImMatGrpClicked)
        self.ui.pushButton_start.clicked.connect(self.on_StartClicked)
        self.ui.pushButton_savepath.clicked.connect(self.on_SavePathClicked)

    def on_ImSetClicked(self):
        # 打开文件选择对话框，只能选择.set文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SET File", "", "SET Files (*.set);;All Files (*)",
                                                   options=options)
        if file_name:
            try:
                set_data = Read_SetData(file_name)
                print(f'Selected file: {file_name}')
                text_name = file_name.split('/')[-1]
                self.ui.lineEdit_filename.setText(text_name)
                self.ui.lineEdit_fileType.setText("set文件")
                self.ui.lineEdit_filepath.setText(file_name)
                self.ui.lineEdit_numTrails.setText(str(set_data.trails_num))
                self.ui.lineEdit_sampleRate.setText(str(set_data.sfreq))
                self.ui.lineEdit_numChannels.setText(str(set_data.channel_num))
                self.ui.lineEdit_samplenum_one.setText(str(set_data.sample_num))
                self.ui.textEdit_InforPrint.setText(file_name + "文件加载完成！\n")
                # 将加载的数据保存在局部变量中
                self.set_file_onedata.append(set_data.get_data())  # 每个trials的数据
                self.set_file_oneevent.append(set_data.get_event_list())  # 每个trials的标签（经过映射的）
                self.ui.textEdit.append("加载数据成功~\n数据形状：{},标签形状：{}".format(self.set_file_onedata[0].shape,
                                                                                        self.set_file_oneevent[
                                                                                            0].shape))
                self.ui.textEdit.append("标签映射关系：{}".format(set_data.get_event_dict()))
                self.event_dict = set_data.get_event_dict()
            except Exception as e:
                print(e)

            # 在这里添加处理选择文件的代码

    def on_ImMatClicked(self):
        # 点击导入单个mat文件
        # 打开文件选择对话框，只能选择.mat文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SET File", "", "SET Files (*.mat);;All Files (*)",
                                                   options=options)
        if file_name:
            try:
                set_data = Read_Mat(file_name)
                print(f'Selected file: {file_name}')
                text_name = file_name.split('/')[-1]
                self.ui.lineEdit_filename.setText(text_name)
                self.ui.lineEdit_fileType.setText("mat文件")
                self.ui.lineEdit_filepath.setText(file_name)
                self.ui.lineEdit_numTrails.setText(str(set_data.trails_num))
                self.ui.lineEdit_sampleRate.setText(str(set_data.sfreq))
                self.ui.lineEdit_numChannels.setText(str(set_data.channel_num))
                self.ui.lineEdit_samplenum_one.setText(str(set_data.sample_num))
                self.ui.textEdit_InforPrint.setText(file_name + "文件加载完成！\n")
                # 将加载的数据保存在局部变量中
                self.mat_file_onedata.append(set_data.get_data())  # 每个trials的数据
                self.mat_file_oneevent.append(np.array(set_data.get_event_list()))  # 每个trials的标签（经过映射的）
                self.ui.textEdit.append("加载数据成功~\n数据形状：{},标签形状：{}".format(self.mat_file_onedata[0].shape,
                                                                                        self.mat_file_oneevent[
                                                                                            0].shape))

                self.ui.textEdit.append("标签映射关系：{}".format(set_data.get_event_dict()))
                self.event_dict = set_data.get_event_dict()
            except Exception as e:
                print(e)

            # 在这里添加处理选择文件的代码

        pass

    def on_ImMatGrpClicked(self):
        # 点击导入多个mat文件
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)

        if folder_path:
            try:
                # 获取该文件夹下的子文件夹，用列表呈现
                # 获取路径下的所有条目
                entries = os.listdir(folder_path)
                # 过滤出文件夹
                folders = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]
                # 呈现格式
                self.ui.lineEdit_filename.setText("{}".format(folders))
                self.ui.lineEdit_filepath.setText(folder_path)
                self.ui.lineEdit_fileType.setText("mat文件组")
                self.ui.textEdit_InforPrint.setText(folder_path + "文件加载完成！\n")

                # 先加载数据到局部变量中，在循环中每次实例化后，计算完成之后都要delete对象以免内存爆炸
                # 这里根据获取的文件夹先构造出被试文件夹路径
                for current_folder in folders:

                    sub_folder_path = os.path.join(folder_path, current_folder)
                    # 读取该路径下的所有mat文件，保存在列表中
                    sub_mat_files = glob.glob(os.path.join(sub_folder_path, "*.mat"))

                    print(sub_mat_files)
                    # 遍历这个列表，依次去取值（最好一个被试文件夹中只有一个文件）
                    # 不支持一个被试多个文件的情况
                    sub_mat_file = sub_mat_files[0]
                    if sub_mat_file:
                        try:
                            current_mat_data = Read_Mat(sub_mat_file)
                            # 将加载的数据保存在局部变量中
                            self.mat_file_grpdata.append(current_mat_data.get_data())  # 每个trials的数据
                            self.mat_file_grpevent.append(np.array(current_mat_data.get_event_list()))  # 每个trials
                            # 的标签（经过映射的）
                            self.ui.textEdit.append(
                                "加载数据成功~\n数据形状：{},标签形状：{}".format(self.mat_file_onedata[0].shape,
                                                                                self.mat_file_grpevent[
                                                                                    0].shape))

                            del current_mat_data


                        except Exception as e:
                            print(e)

                    # 读取文件中的mat文件







            except Exception as e:
                print(e)

    def on_ImSetGrpClicked(self):
        # 点击导入多个set文件
        pass

    def on_SavePathClicked(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.ui.lineEdit.setText(folder_path)

    def on_StartClicked(self):
        if self.single_group:
            # 不是批处理
            if self.ui.lineEdit.text() and self.ui.lineEdit_filepath.text():
                # 如果填写了保存路径
                self.save_path = self.ui.lineEdit.text()
                # 判断是哪种转换类型
                if self.ui.radioButton_setToMat.isChecked():
                    # set转为npz的模式（命名有误，忽略吧）
                    # 读取类内的局部变量进行处理，用单独的函数
                    self.get_single_results(data_list=self.set_file_onedata, event_list=self.set_file_oneevent,
                                            output_dir=self.save_path)
                else:
                    # mat 转换为npz模式
                    self.get_single_results(data_list=self.mat_file_onedata, event_list=self.mat_file_oneevent,
                                            output_dir=self.save_path)
            else:
                QMessageBox.information(self, '提示', '请选择保存路径~')

        else:
            # 是批处理，逻辑更复杂一点，由于读取的文件可能较多，先不直接加载，而是点击执行按钮再加载数据并完成处理
            if self.ui.lineEdit.text() and self.ui.lineEdit_filepath.text():
                # 如果填写了保存路径
                self.save_path = self.ui.lineEdit.text()
                if self.ui.radioButton_setToMat.isChecked():
                    # set转npz模式
                    pass
                else:
                    # mat转npz模式
                    pass
                    # 根据填进文本框中的信息依次读取每个被试的文件

            pass
        # 结束后将变量重置
        self.save_path = ''
        self.set_file_onedata = []
        self.set_file_oneevent = []
        self.mat_file_onedata = []
        self.mat_file_oneevent = []
        self.set_file_grpdata = []
        self.set_file_grpevent = []
        self.mat_file_grpdata = []
        self.mat_file_grpevent = []
        self.event_dict = {}
        self.single_group = True

    def get_single_results(self, data_list, event_list, output_dir):
        # 通过数据列表和标签列表构建npz文件
        # 保存每个样本为单独的 .npz 文件
        data = data_list[0]
        labels = event_list[0]
        for i in range(data.shape[0]):
            file_name = os.path.join(output_dir, f'sample_{i}.npz')
            np.savez(file_name, data=data[i].T, label=labels[i])
            self.ui.textEdit.append("{} 保存完成".format(file_name))

        # 保存标签映射关系
        with open(os.path.join(output_dir, f'event_dict.txt'), 'w') as f:
            dict_str = ', '.join([f'{key}: {value}' for key, value in self.event_dict.items()])
            f.writelines(dict_str)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 创建主窗口实例
    main_window = my_MainWindow()
    # 显示主窗口
    main_window.show()
    sys.exit(app.exec_())
