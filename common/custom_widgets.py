
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt

def _msg_box(title: str, message: str, icon: QMessageBox.Icon):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(icon)
    msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    msg.exec()

def info_msg_box(title: str, message: str):
    _msg_box(title, message, QMessageBox.Icon.Information)

def error_msg_box(title: str, message: str):
    _msg_box(title, message, QMessageBox.Icon.Critical)

def warning_msg_box(title: str, message: str):
    _msg_box(title, message, QMessageBox.Icon.Warning)
