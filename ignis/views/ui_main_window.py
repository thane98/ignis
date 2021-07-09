from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QLabel

from ignis.controllers.fe14_user_config_form import FE14UserConfigForm
from ignis.controllers.inputs_form import InputsForm


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.warning_box = QGroupBox()
        self.warning_label = QLabel(
            "NOTE: Randomizing the same files repeatedly can lead to a buggy game. "
            "For the best results, start with a clean output folder."
        )
        self.warning_label.setWordWrap(True)

        warning_layout = QVBoxLayout()
        warning_layout.addWidget(self.warning_label)
        self.warning_box.setLayout(warning_layout)

        self.inputs_form = InputsForm()
        self.randomize_button = QPushButton("Randomize")
        self.randomize_button.setEnabled(False)
        self.randomizer_config = FE14UserConfigForm()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.warning_box)
        layout.addWidget(self.inputs_form)
        layout.addWidget(self.randomizer_config)
        layout.addWidget(self.randomize_button)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        self.setFixedSize(650, 625)

        self.setWindowIcon(QIcon("ignis.ico"))
        self.setWindowTitle("Ignis - FE14 Randomizer")
