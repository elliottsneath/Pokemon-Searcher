import sys
import traceback
import datetime

from PySide6.QtCore import QLoggingCategory
from common.custom_widgets import error_msg_box

def suppress_qt_warnings() -> None:
    QLoggingCategory.setFilterRules("qt.gui.imageio=false")

def install_exception_hook() -> None:
    def exception_hook(type_, value, tb):
        time_stamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        traceback_text = f"{time_stamp} -- ".join(traceback.format_exception(type_, value, tb))
        with open("error_log.txt", "a") as log_file:
            log_file.write(traceback_text)
        error_msg_box("Error", f"An unexpected error occurred:\n\n{type_.__name__}: {value}\n\nSee error log for details.")
        traceback.print_exception(type_, value, tb)
    sys.excepthook = exception_hook
