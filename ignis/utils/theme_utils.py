from PySide6.QtGui import QPalette, QColor, Qt, QFont


def gen_font() -> QFont:
    font = QFont()
    font.setPointSize(10)
    return font


def gen_dark_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.PlaceholderText, QColor(189, 189, 189))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    return palette
