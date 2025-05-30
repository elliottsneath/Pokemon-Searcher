from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor

class StatBar(QWidget):
    def __init__(self, value=0, max_value=100, color=QColor("orange")):
        super().__init__()
        self.value = value
        self.max_value = max_value
        self.color = color
        self.setFixedHeight(10)

    def set_value(self, value,  max_stat):
        """Update the value of the stat bar."""
        self.value = value
        self.max_value = max_stat
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        bar_width = int((self.value / self.max_value) * self.width())
        painter.setBrush(self.color)
        painter.drawRect(0, 0, bar_width, self.height())