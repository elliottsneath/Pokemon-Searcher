from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, Property, QEasingCurve
from PySide6.QtGui import QColor

class AnimatedHoverButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self._color_value = 0.0
        
        # Create the animation
        self._animation = QPropertyAnimation(self, b"hover_progress", self)
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Store colors
        self.original_color = self.palette().button().color()
        if not is_windows_dark_mode():
            self.original_color = QColor("#e3e3e3")
        self.hover_color = QColor("#819FFF")
        
        # Initial style
        self.setAutoFillBackground(True)
        self.updateStyleSheet(0.0)
        
    def get_hover_progress(self):
        return self._color_value
        
    def set_hover_progress(self, value):
        self._color_value = value
        self.updateStyleSheet(value)
        
    hover_progress = Property(float, get_hover_progress, set_hover_progress)
    
    def updateStyleSheet(self, value):
        color = self.interpolateColor(self.original_color, self.hover_color, value)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                padding: 4px;
                margin: 1px;
                border: 0px solid #999;
                border-radius: 6px;
            }}
        """)
    
    def interpolateColor(self, color_start, color_end, fraction):
        r = int(color_start.red() + (color_end.red() - color_start.red()) * fraction)
        g = int(color_start.green() + (color_end.green() - color_start.green()) * fraction)
        b = int(color_start.blue() + (color_end.blue() - color_start.blue()) * fraction)
        return QColor(r, g, b)
        
    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._color_value)
        self._animation.setEndValue(1.0)
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._color_value)
        self._animation.setEndValue(0.0)
        self._animation.start()
        super().leaveEvent(event)


def is_windows_dark_mode():
        try:
            import winreg
        except ImportError:
            return False

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key_name = "AppsUseLightTheme"

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, key_name)
                return value == 0  # 0 means dark mode is enabled
        except FileNotFoundError:
            return False
        except WindowsError:
            return False