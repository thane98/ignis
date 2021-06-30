import os
import traceback

from PySide6.QtCore import QObject, Signal, QRunnable

from ignis.core.fe14.fe14_randomization_process import FE14RandomizationProcess
from ignis.model.game import Game

from ignis import ignis as ign
from ignis.model.game_load_inputs import GameLoadInputs


class RandomizeWorker(QObject, QRunnable):
    finished = Signal()
    error = Signal(object, str)

    def __init__(self, inputs: GameLoadInputs, game_config, user_config):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.inputs = inputs
        self.game_config = game_config
        self.user_config = user_config

    def run(self):
        config_root = os.path.join(os.getcwd(), "Data", self.inputs.game)
        try:
            gd = ign.GameData.load(
                self.inputs.output_path,
                self.inputs.rom_path,
                self.inputs.game,
                self.inputs.language,
                config_root,
            )
            gd.read()

            if self.inputs.game == Game.FE14:
                process = FE14RandomizationProcess(
                    gd,
                    self.user_config,
                    self.game_config,
                    self.inputs.rom_path,
                    self.inputs.output_path,
                )
            else:
                raise NotImplementedError(
                    "Randomization is not supported for the given game."
                )

            process.randomize()

            self.finished.emit()
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(e, tb)
