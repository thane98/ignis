from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ignis.controllers.fe14_user_config_form import FE14UserConfigForm
from ignis.controllers.inputs_form import InputsForm


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.inputs_form = InputsForm()
        self.randomize_button = QPushButton("Randomize")
        self.randomize_button.setEnabled(False)
        self.randomizer_config = FE14UserConfigForm()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.inputs_form)
        layout.addWidget(self.randomizer_config)
        layout.addWidget(self.randomize_button)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        self.setFixedSize(650, 450)

        self.setWindowIcon(QIcon("ignis.ico"))
        self.setWindowTitle("Ignis - FE14 Randomizer")
