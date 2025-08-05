
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from utils import generate_pattern_image, calculate_moire_intensity, quantize_intensity, generate_heatmap
import numpy as np
import cv2

class MoireViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {'freq1': 10, 'angle1': 0, 'freq2': 11, 'angle2': 5, 'size': 512}

        self.image_label = QLabel()
        self.heatmap_label = QLabel()
        self.intensity_label = QLabel()
        self.quantization_label = QLabel()

        self.slider_freq1 = QSlider(Qt.Horizontal)
        self.slider_freq1.setRange(1, 100)
        self.slider_freq1.setValue(self.params['freq1'])
        self.slider_freq1.valueChanged.connect(self.update_from_slider)

        self.chart = QChart()
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart_view = QChartView(self.chart)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.heatmap_label)
        layout.addWidget(self.intensity_label)
        layout.addWidget(self.quantization_label)
        layout.addWidget(self.slider_freq1)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

        self.step = 0
        self.update_view()

    def update_from_slider(self, value):
        self.params['freq1'] = value
        self.update_view()

    def update_parameters(self, new_params):
        self.params.update(new_params)
        self.slider_freq1.setValue(self.params['freq1'])
        self.update_view()

    def update_view(self):
        size = self.params['size']
        moire = generate_pattern_image(self.params['freq1'], self.params['angle1'], self.params['freq2'], self.params['angle2'], size)
        self.image = moire

        self.intensity = calculate_moire_intensity(moire)
        self.quantized = quantize_intensity(self.intensity)
        self.heatmap = generate_heatmap(moire)

        self.image_label.setPixmap(QPixmap.fromImage(QImage(moire.data, size, size, size, QImage.Format.Format_Grayscale8)))
        h, w, _ = self.heatmap.shape
        qheatmap = QImage(self.heatmap.data, w, h, 3*w, QImage.Format.Format_RGB888)
        self.heatmap_label.setPixmap(QPixmap.fromImage(qheatmap))

        self.intensity_label.setText(f"Moire Intensity: {self.intensity:.2f}")
        self.quantization_label.setText(f"Quantized Value: {self.quantized}")

        self.series.append(self.step, self.intensity)
        self.step += 1
