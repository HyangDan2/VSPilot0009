
from PySide6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QSpinBox, QComboBox

class ParameterDialog(QDialog):
    def __init__(self, params: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Pattern Parameters")

        self.freq1 = QSpinBox()
        self.freq1.setRange(1, 1000)
        self.freq1.setValue(params.get('freq1', 11)) 

        self.angle1 = QSpinBox()
        self.angle1.setRange(0, 180)
        self.angle1.setValue(params.get('angle1', 0))

        self.freq2 = QSpinBox()
        self.freq2.setRange(1, 1000)
        self.freq2.setValue(params.get('freq2', 10)) 

        self.angle2 = QSpinBox()
        self.angle2.setRange(0, 180)
        self.angle2.setValue(params.get('angle2', 5))

        self.pattern1_combo = QComboBox()
        self.pattern1_combo.addItems(["sin", "square", "triangle", "checker"])

        self.pattern2_combo = QComboBox()
        self.pattern2_combo.addItems(["sin", "square", "triangle", "checker"])


        layout = QFormLayout(self)
        layout.addRow("Frequency 1", self.freq1)
        layout.addRow("Angle 1", self.angle1)
        layout.addRow("Frequency 2", self.freq2)
        layout.addRow("Angle 2", self.angle2)
        layout.addRow("Pattern Type 1", self.pattern1_combo)
        layout.addRow("Pattern Type 2", self.pattern2_combo)
        self.pattern1_combo.setCurrentText(params.get("pattern_type1", "sin"))
        self.pattern2_combo.setCurrentText(params.get("pattern_type2", "sin"))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_params(self):
        return {
            'freq1': self.freq1.value(),
            'angle1': self.angle1.value(),
            'freq2': self.freq2.value(),
            'angle2': self.angle2.value(),
            'pattern_type1': self.pattern1_combo.currentText(),
            'pattern_type2': self.pattern2_combo.currentText(),
            'size': 512
        }
