
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QHBoxLayout, QSpinBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from sources.utils import generate_pattern_image, calculate_moire_intensity, quantize_intensity, generate_heatmap
import numpy as np
import cv2

class MoireViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {'freq1': 10, 'angle1': 0, 'freq2': 11, 'angle2': 5, 
                       'pattern_type1' : 'sin', 'pattern_type2' : 'sin', 'size': 512}


        # ---- 위쪽 4단 이미지/라벨 구역 ----
        self.image_label = QLabel("Moire Image")
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(256, 256)

        self.heatmap_label = QLabel("FFT Heatmap")
        self.heatmap_label.setScaledContents(True)
        self.heatmap_label.setFixedSize(256, 256)

        self.intensity_label = QLabel("Intensity")
        self.intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intensity_label.setFixedSize(256, 256)

        self.quantization_label = QLabel("Quantized")
        self.quantization_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quantization_label.setFixedSize(256, 256)

        top_row = QHBoxLayout()
        top_row.addWidget(self.image_label)
        top_row.addWidget(self.heatmap_label)
        top_row.addWidget(self.intensity_label)
        top_row.addWidget(self.quantization_label)
        
        self.slider_freq1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_freq1.setRange(1, 100)
        self.slider_freq1.setValue(self.params['freq1'])
        self.slider_freq1.valueChanged.connect(self.update_from_slider)
        
        self.slider_angle1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_angle1.setRange(-90, 90)
        self.slider_angle1.setValue(self.params['angle1'])
        self.slider_angle1.valueChanged.connect(self.update_from_slider_angle1)

        self.chart = QChart()
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()

        self.chart_view = QChartView(self.chart)
        self.chart_view.setMinimumHeight(200)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_row)
        main_layout.addWidget(self.slider_freq1)
        main_layout.addWidget(self.slider_angle1)
        main_layout.addWidget(self.chart_view)

        self.setLayout(main_layout)

        self.step = 0
        self.update_view()

    def update_from_slider(self, value):
        self.params['freq1'] = value
        self.update_view()

    def update_from_slider_angle1(self, value):
        self.params['angle1'] = value
        self.update_view()

    def update_parameters(self, new_params):
        self.params.update(new_params)
        self.slider_freq1.setValue(self.params['freq1'])
        self.update_view()

    def update_view(self):
        size = self.params['size']
        moire = generate_pattern_image(self.params, size)
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
