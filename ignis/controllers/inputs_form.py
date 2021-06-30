from PySide6.QtCore import Signal

from ignis.model.game_load_inputs import GameLoadInputs
from ignis.views.ui_inputs_form import Ui_InputsForm


class InputsForm(Ui_InputsForm):
    updated = Signal(bool)

    def __init__(self):
        super().__init__()

        self.game_box.setCurrentIndex(0)
        self.game_box.setEnabled(False)

        self.romfs_path_input.selection_changed.connect(self._on_update)
        self.output_path_input.selection_changed.connect(self._on_update)
        self.game_box.currentIndexChanged.connect(self._on_update)
        self.language_box.currentIndexChanged.connect(self._on_update)

        self.language_box.setCurrentIndex(1)

    def _on_update(self):
        self.updated.emit(self.fields_are_valid())

    def fields_are_valid(self) -> bool:
        return bool(
            self.romfs_path_input.text
            and self.output_path_input.text
            and self.game_box.value()
            and self.language_box.value()
        )

    def inputs(self) -> GameLoadInputs:
        if not self.fields_are_valid():
            raise RuntimeError("Called inputs with invalid fields.")
        return GameLoadInputs(
            rom_path=self.romfs_path_input.text,
            output_path=self.output_path_input.text,
            game=self.game_box.value(),
            language=self.language_box.value(),
        )
