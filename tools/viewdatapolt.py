import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EEGPlotWidget(QWidget):
    def __init__(self, eeg_data, fs=250, window_sec=5, parent=None):
        super().__init__(parent)
        self.eeg_data = eeg_data  # shape: n_samples x n_channels
        self.fs = fs
        self.window_sec = window_sec
        self.window_size = fs * window_sec
        self.start_idx = 0

        self.n_samples, self.n_channels = eeg_data.shape

        self.init_ui()
        self.plot_data()

    def init_ui(self):
        layout = QVBoxLayout()

        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Slider setup
        self.slider = QSlider(Qt.Horizontal)
        max_start = max(0, self.n_samples - self.window_size)
        self.slider.setMaximum(max_start)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(self.fs)  # slide by 1 second
        self.slider.valueChanged.connect(self.on_slider_moved)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def plot_data(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        end_idx = self.start_idx + self.window_size
        time_axis = np.arange(self.start_idx, end_idx) / self.fs
        segment = self.eeg_data[self.start_idx:end_idx, :]

        for i in range(self.n_channels):
            ax.plot(time_axis, segment[:, i] + i * 100, label=f'Ch{i+1}')  # offset each channel vertically

        ax.set_title("EEG Signals")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Channels")
        ax.set_yticks([i * 100 for i in range(self.n_channels)])
        ax.set_yticklabels([f'Ch{i+1}' for i in range(self.n_channels)])
        ax.grid(True)
        self.canvas.draw()

    def on_slider_moved(self, value):
        self.start_idx = value
        self.plot_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 生成模拟数据：10秒，采样率250Hz，8通道
    n_samples = 2500
    n_channels = 8
    fs = 250
    eeg_data = np.random.randn(n_samples, n_channels) * 50  # 模拟数据

    win = EEGPlotWidget(eeg_data, fs=fs, window_sec=5)
    win.setWindowTitle("EEG Viewer with Scroll")
    win.resize(1000, 600)
    win.show()

    sys.exit(app.exec_())
