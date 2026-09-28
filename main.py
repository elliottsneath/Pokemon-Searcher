import sys
import ctypes

from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QSplashScreen
from PySide6.QtGui import Qt, QPixmap, QIcon
from PySide6.QtCore import Signal

from assets.ui.main_ui import Ui_PokemonSearcher
from assets.ui.help_popup_ui import Ui_helpDialog
from common.version_control import VersionControl, APP_NAME
from common.widget_groups import MainWidgets, SettingsWidgets
from common.handlers.data_handler import DataHandler
from common.handlers.pokemon_list_handler import PokemonListHandler
from common.handlers.settings_handler import SettingsHandler
from common.helpers import install_exception_hook

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
install_exception_hook()

class MainWindow(QMainWindow, Ui_PokemonSearcher):
    loaded = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Pokemon Draft Searcher")

        self._init_vars()
        self.data_handler = DataHandler(self)
        self.pokemon_list_handler = PokemonListHandler(self, MainWidgets(self))
        self.settings_handler = SettingsHandler(self, SettingsWidgets(self))

        self.actionSettings.triggered.connect(lambda: self.toggle_settings(1))
        self.actionHelp.triggered.connect(self.show_help)

        self.pokemon_list_handler.update()
        self.version_control = VersionControl(self.actionVersion, self.versionStatusBar)
        self.loaded.emit()

    def _init_vars(self) -> None:
        self.master_list = []
        self.all_names = []
        self.all_moves = set()
        self.all_types = [
            "Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying",
            "Ghost", "Grass", "Ground", "Ice", "Normal", "Psychic", "Poison", "Rock",
            "Steel", "Water",
        ]
        self.all_abilities = set()
        self.draft_board = {}
        self.draft_pools = 0
        self.pool = None
        self.hide_drafted = False
        self.selected_pokemon = []
        self.pokedex = []
        self.highest_stats = [-float('inf')] * 6
        self.lowest_stats = [float('inf')] * 6

    def toggle_settings(self, i: int) -> None:
        self.stackedWidget.setCurrentIndex(i)

    def show_help(self) -> None:
        dialog = QDialog(self)
        ui = Ui_helpDialog()
        ui.setupUi(dialog)
        dialog.exec()

    def closeEvent(self, event) -> None:
        try:
            self.data_handler.save_config()
        except Exception as e:
            print(f"Error saving config: {e}")
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icons/pokemon_searcher.ico'))
    icon = QPixmap('assets/icons/pokemon_searcher.png')
    spl = QSplashScreen(icon.scaled(icon.size() * 0.5, Qt.KeepAspectRatio))
    spl.show()
    spl.activateWindow()
    window = MainWindow()
    window.loaded.connect(lambda: spl.finish(window))
    window.show()
    spl.finish(window)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
