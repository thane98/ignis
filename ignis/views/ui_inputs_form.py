from PySide6 import QtGui
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar,
)

from ignis.controllers.directory_input import DirectoryInput
from ignis.controllers.enum_combo_box import EnumComboBox
from ignis.model.game import Game
from ignis.model.language import Language


class Ui_InputsForm(QWidget):
    def __init__(self):
        super().__init__()

        self.romfs_path_input = DirectoryInput("Extracted RomFS path...")
        self.output_path_input = DirectoryInput("Output path...")
        self.paths_layout = QVBoxLayout()
        self.paths_layout.addWidget(self.romfs_path_input)
        self.paths_layout.addWidget(self.output_path_input)
        self.paths_group_box = QGroupBox("Paths")
        self.paths_group_box.setLayout(self.paths_layout)

        self.game_box = EnumComboBox(Game)
        self.game_box.setPlaceholderText("Select game...")
        self.language_box = EnumComboBox(Language)
        self.language_box.setPlaceholderText("Select language...")
        self.rom_info_layout = QVBoxLayout()
        self.rom_info_layout.addWidget(self.game_box)
        self.rom_info_layout.addWidget(self.language_box)
        self.rom_info_box = QGroupBox("ROM Info.")
        self.rom_info_box.setLayout(self.rom_info_layout)

        boxes_layout = QHBoxLayout()
        boxes_layout.setContentsMargins(0, 0, 0, 0)
        boxes_layout.addWidget(self.paths_group_box)
        boxes_layout.addWidget(self.rom_info_box)
        self.setLayout(boxes_layout)
