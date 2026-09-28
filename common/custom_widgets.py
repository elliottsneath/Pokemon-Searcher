import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
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
