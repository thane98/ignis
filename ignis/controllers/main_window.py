import logging

from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QProgressDialog

from ignis.core.randomize_worker import RandomizeWorker
from ignis.model.configs import Configs
from ignis.model.fe14_route_exception import FE14RouteException
from ignis.utils import dialog_utils
from ignis.views.ui_main_window import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    def __init__(self, configs: Configs):
        super().__init__()

        self.configs = configs
        self.thread_pool = QThreadPool()
        self.load_worker = None

        self.progress_dialog = None

        self.inputs_form.updated.connect(self._on_config_form_updated)
        self.randomizer_config.updated.connect(self._on_config_form_updated)
        self.randomize_button.clicked.connect(self._on_randomize_clicked)

        self._on_config_form_updated()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.thread_pool.deleteLater()
        super().closeEvent(event)

    def _on_config_form_updated(self):
        self.randomize_button.setEnabled(
            self.inputs_form.fields_are_valid()
            and self.randomizer_config.fields_are_valid()
        )

    def _on_randomize_clicked(self):
        inputs = self.inputs_form.inputs()
        game_config = self.configs.fe14_config  # We only support FE14 right now.
        user_config = self.randomizer_config.config()

        logging.info(f"Loading inputs={inputs}")
        self.load_worker = RandomizeWorker(inputs, game_config, user_config)
        self.load_worker.finished.connect(self._on_randomize_success)
        self.load_worker.error.connect(self._on_randomize_failure)
        self.randomize_button.setEnabled(False)
        self.thread_pool.start(self.load_worker)

        self.progress_dialog = QProgressDialog()
        self.progress_dialog.setWindowTitle("Randomizing...")
        self.progress_dialog.setWindowIcon(QIcon("ignis.ico"))
        self.progress_dialog.setRange(0, 0)
        self.progress_dialog.show()

    def _on_randomize_success(self):
        self.progress_dialog.hide()
        dialog_utils.info(
            "Randomizing Succeeded! Check the output folder for a full report.",
            "Success!",
        )
        self.randomize_button.setEnabled(True)

    def _on_randomize_failure(self, e, tb):
        self.progress_dialog.hide()
        if isinstance(e, FE14RouteException):
            dialog_utils.error(
                self,
                message=f"Your ROM does not have the data for route {e.route.name}.",
            )
        else:
            dialog_utils.error(self, tb)
        self.randomize_button.setEnabled(True)
