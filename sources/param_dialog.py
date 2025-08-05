
from PySide6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QSpinBox

class ParameterDialog(QDialog):
    def __init__(self, params, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Pattern Parameters")

        self.freq1 = QSpinBox()
        self.freq1.setRange(1, 100)
        self.freq1.setValue(params['freq1'])

        self.angle1 = QSpinBox()
        self.angle1.setRange(0, 180)
        self.angle1.setValue(params['angle1'])

        self.freq2 = QSpinBox()
        self.freq2.setRange(1, 100)
        self.freq2.setValue(params['freq2'])

        self.angle2 = QSpinBox()
        self.angle2.setRange(0, 180)
        self.angle2.setValue(params['angle2'])

        layout = QFormLayout(self)
        layout.addRow("Frequency 1", self.freq1)
        layout.addRow("Angle 1", self.angle1)
        layout.addRow("Frequency 2", self.freq2)
        layout.addRow("Angle 2", self.angle2)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_params(self):
        return {
            'freq1': self.freq1.value(),
            'angle1': self.angle1.value(),
            'freq2': self.freq2.value(),
            'angle2': self.angle2.value(),
            'size': 512
        }
