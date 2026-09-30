import os

from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget

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


def type_count_widget(type_name: str, label: str, parent: QWidget = None) -> QWidget:
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
    widget.setStyleSheet("background-color: rgba(0,0,0,0.45); border-radius: 10px;")

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(4, 2, 6, 2)
    layout.setSpacing(4)

    icon = QLabel()
    pix = QPixmap(os.path.join("assets", "icons", f"{type_name.lower()}.svg"))
    if not pix.isNull():
        icon.setPixmap(pix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    else:
        icon.setText(type_name)
    layout.addWidget(icon)

    lbl = QLabel(f"{type_name.upper()} {label}")
    lbl.setStyleSheet("font-size: 10px; font-weight: bold; background: transparent;")
    layout.addWidget(lbl)

    return widget


def recommendation_card_widget(
    name: str,
    types: list[str],
    cost: "int | None",
    reasons: list[str],
    sprite: "QPixmap | None",
    on_add,
    parent: QWidget = None,
) -> QWidget:
    widget = QWidget(parent)
    widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
    widget.setStyleSheet("background-color: rgba(255,255,255,0.05); border-radius: 6px;")

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(6, 4, 6, 4)
    layout.setSpacing(8)

    sprite_lbl = QLabel()
    sprite_lbl.setFixedSize(48, 48)
    sprite_lbl.setAlignment(Qt.AlignCenter)
    if sprite and not sprite.isNull():
        sprite_lbl.setPixmap(sprite.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    layout.addWidget(sprite_lbl)

    info = QVBoxLayout()
    info.setSpacing(2)

    name_lbl = QLabel(name)
    name_lbl.setStyleSheet("font-weight: bold; font-size: 11px; background: transparent;")
    info.addWidget(name_lbl)

    types_row = QWidget()
    types_row.setStyleSheet("background: transparent;")
    types_layout = QHBoxLayout(types_row)
    types_layout.setContentsMargins(0, 0, 0, 0)
    types_layout.setSpacing(2)
    for t in types:
        t_lbl = QLabel()
        t_lbl.setStyleSheet("background: transparent;")
        pix = QPixmap(os.path.join("assets", "icons", f"{t.lower()}.svg"))
        if not pix.isNull():
            t_lbl.setPixmap(pix.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            t_lbl.setText(t)
        types_layout.addWidget(t_lbl)
    types_layout.addStretch()
    info.addWidget(types_row)

    reason_lbl = QLabel(", ".join(reasons))
    reason_lbl.setStyleSheet("font-size: 9px; color: rgba(255,255,255,0.55); background: transparent;")
    reason_lbl.setWordWrap(True)
    info.addWidget(reason_lbl)

    layout.addLayout(info)
    layout.addStretch()

    right = QVBoxLayout()
    right.setSpacing(4)
    right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    pts_lbl = QLabel(f"{cost} pts" if cost is not None else "")
    pts_lbl.setStyleSheet("font-size: 10px; font-weight: bold; background: transparent;")
    pts_lbl.setAlignment(Qt.AlignRight)
    right.addWidget(pts_lbl)

    add_btn = QPushButton("ADD")
    add_btn.setFixedWidth(52)
    add_btn.clicked.connect(on_add)
    right.addWidget(add_btn)

    layout.addLayout(right)

    return widget


_HANDLE_R = 7
_TRACK_H = 4


class RangeSlider(QWidget):
    value_changed = Signal(int, int)    # fires every drag tick — use for live label updates
    range_committed = Signal(int, int)  # fires on mouse release — use for expensive updates

    def __init__(self, parent=None, minimum: int = 0, maximum: int = 100):
        super().__init__(parent)
        self._min = minimum
        self._max = maximum
        self._low = minimum
        self._high = maximum
        self._pressed: str | None = None  # "low" | "high"
        self.setMinimumHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    @property
    def low(self) -> int:
        return self._low

    @property
    def high(self) -> int:
        return self._high

    def setOrientation(self, _) -> None:
        pass

    def set_range(self, minimum: int, maximum: int) -> None:
        self._min = minimum
        self._max = maximum
        self._low = max(minimum, min(self._low, maximum))
        self._high = max(minimum, min(self._high, maximum))
        self.update()

    def set_value(self, low: int, high: int) -> None:
        self._low = max(self._min, min(low, self._max))
        self._high = max(self._low, min(high, self._max))
        self.update()

    def _val_to_x(self, value: int) -> float:
        span = self._max - self._min
        if span == 0:
            return float(_HANDLE_R)
        return _HANDLE_R + (value - self._min) / span * (self.width() - 2 * _HANDLE_R)

    def _x_to_val(self, x: float) -> int:
        usable = self.width() - 2 * _HANDLE_R
        if usable <= 0:
            return self._min
        frac = max(0.0, min(1.0, (x - _HANDLE_R) / usable))
        return round(self._min + frac * (self._max - self._min))

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cy = self.height() - _HANDLE_R - 4

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 255, 255, 40))
        p.drawRoundedRect(_HANDLE_R, cy - _TRACK_H // 2,
                          self.width() - 2 * _HANDLE_R, _TRACK_H, 2, 2)

        lx = self._val_to_x(self._low)
        hx = self._val_to_x(self._high)
        p.setBrush(QColor(100, 160, 255, 200))
        p.drawRect(int(lx), cy - _TRACK_H // 2, int(hx - lx), _TRACK_H)

        for x in (lx, hx):
            p.setBrush(QColor(230, 230, 230))
            p.setPen(QPen(QColor(150, 150, 150), 1))
            p.drawEllipse(QPointF(x, cy), _HANDLE_R, _HANDLE_R)

        font = p.font()
        font.setPointSize(8)
        p.setFont(font)
        p.setPen(QColor(255, 255, 255, 200))
        text_h = cy - _HANDLE_R - 2
        for x, val in ((lx, self._low), (hx, self._high)):
            rx = max(0, min(int(x - 20), self.width() - 40))
            p.drawText(rx, 0, 40, text_h,
                       Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                       str(val))

        p.end()

    def _closest_handle(self, x: float) -> str:
        return "low" if abs(x - self._val_to_x(self._low)) <= abs(x - self._val_to_x(self._high)) else "high"

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self._pressed = self._closest_handle(event.position().x())
        self._drag(event.position().x())

    def mouseMoveEvent(self, event) -> None:
        if self._pressed:
            self._drag(event.position().x())
            return
        x = event.position().x()
        if abs(x - self._val_to_x(self._low)) <= _HANDLE_R + 2 or \
                abs(x - self._val_to_x(self._high)) <= _HANDLE_R + 2:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.unsetCursor()

    def mouseReleaseEvent(self, event) -> None:
        if self._pressed:
            self._pressed = None
            self.range_committed.emit(self._low, self._high)

    def reset(self) -> None:
        self.set_value(self._min, self._max)

    def _drag(self, x: float) -> None:
        val = self._x_to_val(x)
        if self._pressed == "low":
            self._low = min(val, self._high)
        else:
            self._high = max(val, self._low)
        self.value_changed.emit(self._low, self._high)
        self.update()
