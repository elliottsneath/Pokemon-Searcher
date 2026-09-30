"""In-app debug panel: a dockable QTextEdit that captures stdout/stderr and displays coloured log output."""

import sys
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat
from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton


class _Stream(QObject):
    written = Signal(str)

    def write(self, text):
        if text:
            self.written.emit(text)

    def flush(self):
        pass


class DebugPanel(QDockWidget):
    def __init__(self, main_window):
        super().__init__("Debug Output", main_window)
        self.setObjectName("DebugPanel")
        self.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.addStretch()
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedHeight(22)
        clear_btn.setFixedWidth(60)
        clear_btn.clicked.connect(self._clear)
        toolbar.addWidget(clear_btn)
        layout.addLayout(toolbar)

        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setFont(QFont("Consolas", 9))
        self._output.setStyleSheet(
            "QTextEdit { background-color: #1e1e1e; color: #d4d4d4; border: none; }"
        )
        layout.addWidget(self._output)

        self.setWidget(container)
        self.hide()

        self._stdout_stream = _Stream()
        self._stderr_stream = _Stream()
        self._stdout_stream.written.connect(self._write)
        self._stderr_stream.written.connect(lambda t: self._write(t, error=True))
        sys.stdout = self._stdout_stream
        sys.stderr = self._stderr_stream

    def _write(self, text, error=False):
        cursor = self._output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("#f48771" if error else "#d4d4d4"))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        self._output.setTextCursor(cursor)
        self._output.ensureCursorVisible()

    def _clear(self):
        self._output.clear()
