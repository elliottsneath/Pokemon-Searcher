from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("padding: 5px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def highlight(self, on=True):
        if on:
            self.setStyleSheet("background-color: rgba(94, 94, 94, 0.8); font-weight: bold; padding: 5px;")
        else:
            self.setStyleSheet("background-color: none; font-weight: normal; padding: 5px;")

    def change_star(self, fill: bool):
        star_png = "star_filled.png" if fill else "star.png"
        png_path = os.path.join("assets", "icons", star_png)
        self.setPixmap(QPixmap(png_path).scaled(36, 36))