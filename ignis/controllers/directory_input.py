from typing import Optional
from PySide6.QtWidgets import QFileDialog
from ignis.views.ui_directory_input import Ui_DirectoryInput


class DirectoryInput(Ui_DirectoryInput):
    def __init__(self, placeholder_text=None, parent=None):
        super().__init__(placeholder_text, parent)
        self.open_dialog_button.clicked.connect(self._on_open_dialog_clicked)

    @property
    def text(self):
        return self.line_edit.text()

    @property
    def selection_changed(self):
        return self.line_edit.textChanged

    def set_text(self, text: Optional[str]):
        self.line_edit.setText(text)

    def _on_open_dialog_clicked(self):
        dialog = QFileDialog()
        f = dialog.getExistingDirectory(parent=self, caption="Select a directory...")
        if f:
            self.set_text(f)
