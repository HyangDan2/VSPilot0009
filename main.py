
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QStatusBar
from PySide6.QtGui import QAction
from sources.moire_viewer import MoireViewer
from sources.param_dialog import ParameterDialog
from sources.config_handler import save_params_to_json, load_params_from_json
from sources.file_handler import save_all_result
import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moire Pattern Viewer")
        self.viewer = MoireViewer()
        self.setCentralWidget(self.viewer)
        self._create_menu()
        self.setStatusBar(QStatusBar())

    def _create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        save_all_action = QAction("Save All", self)
        save_all_action.triggered.connect(self.save_all)
        file_menu.addAction(save_all_action)

        edit_menu = menubar.addMenu("Edit")
        param_action = QAction("Set Parameters", self)
        param_action.triggered.connect(self.open_param_dialog)
        edit_menu.addAction(param_action)

        load_action = QAction("Load Previous Parameters", self)
        load_action.triggered.connect(self.load_previous_params)
        edit_menu.addAction(load_action)

    def open_param_dialog(self):
        dialog = ParameterDialog(self.viewer.params, self)
        if dialog.exec():
            new_params = dialog.get_params()
            self.viewer.update_parameters(new_params)
            save_params_to_json(new_params)

    def load_previous_params(self):
        loaded = load_params_from_json()
        if loaded:
            self.viewer.update_parameters(loaded)
            self.statusBar().showMessage("🔁 설정이 복원되었습니다!", 3000)
        else:
            self.statusBar().showMessage("⚠️ 이전 설정이 없습니다.", 3000)

    def save_all(self):
        save_all_result("logs", self.viewer.image, self.viewer.heatmap, self.viewer.series)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
