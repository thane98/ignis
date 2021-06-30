import traceback

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

from ignis.controllers.error_dialog import ErrorDialog


def error(window=None, message=None):
    message = message if message else traceback.format_exc()
    if window:
        window.error_dialog = ErrorDialog(message)
        window.error_dialog.show()
    else:
        error_dialog = ErrorDialog(message)
        error_dialog.exec_()


def warning(text, title):
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setWindowTitle(title)
    message_box.setWindowIcon(QIcon("ignis.ico"))
    message_box.setIcon(QMessageBox.Warning)
    message_box.exec_()


def info(text, title):
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setWindowTitle(title)
    message_box.setWindowIcon(QIcon("ignis.ico"))
    message_box.setIcon(QMessageBox.Information)
    message_box.exec_()
