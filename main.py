import sys
import json
import os
from assets.ui.pokemon_list_item import PokemonListItem, SettingsPokemonListItem
from data.pokemon_obj import PokemonData
from assets.ui.main_ui import Ui_PokemonSearcher
from assets.ui.pokemon_popup_ui import Ui_PokemonPopup
from assets.ui.clickable_label import ClickableLabel
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QCompleter, QWidget, \
                              QHBoxLayout, QDialog, QLabel, QSizePolicy, QSplashScreen, \
                              QMessageBox, QFileDialog, QTextEdit, QVBoxLayout, QPushButton
from PySide6.QtGui import Qt, QPixmap, QColor, QIcon, QMovie
from PySide6.QtCore import QStringListModel, QTimer, Signal, QSize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

POKEDEX_PATH = os.path.join(BASE_DIR, "data/pokedex.json")
LEARNSET_PATH = os.path.join(BASE_DIR, "data/learnsets.json")
SELECTED_POKEMON_PATH = os.path.join(BASE_DIR, "data/selected_pokemon.json")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "data/config.json")

"""
TODO:
- import from google sheet
- import from text
- fix splash screen
- update pokemon learnset based on evos
"""

class MainWindow(QMainWindow, Ui_PokemonSearcher):
    loaded = Signal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("One Pointer Pokemon Searcher")

        self.initialise_vars()
        self.initialise_completer()
        self.initialise_connections()
        self.initialise_spinner()

        self.update_filtered_pokemon()

        self.loaded.emit()

    def initialise_vars(self):
        self.master_list = []
        self.filtered_sorted_list = []
        self.applied_filters = []
        self.selected_trait = None
        self.trait_reverse = True

        self.all_names = []
        self.all_moves = set()
        self.all_types = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying",
                         "Ghost", "Grass", "Ground", "Ice", "Normal", "Psychic", "Poison", "Rock",
                         "Steel", "Water"]
        self.all_abilities = set()

        self.load_pokemon_data()

    def load_pokemon_data(self, init = True):
        try:
            with open(POKEDEX_PATH, 'r') as f:
                pokedex = json.load(f)
            with open(SELECTED_POKEMON_PATH, 'r') as f:
                if init:
                    data = json.load(f)
                    self.selected_pokemon = data.get("selected_pokemon", [])
            with open(LEARNSET_PATH, 'r') as f:
                learnset_data = json.load(f)
            with open(CONFIG_FILE_PATH, 'r') as f:
                favourites = json.load(f)

            self.highest_stats = [-float('inf')] * 6
            self.lowest_stats = [float('inf')] * 6
            if init:
                self.pokedex = []
            for pokemon, data in pokedex.items():

                # ------ SETTINGS POKEDEX ------
                if init:
                    num = data.get("num", -1)
                    name = data.get("name", "")
                    self.pokedex.append(pokemon)
                    custom_widget = SettingsPokemonListItem(pokemon)
                    if pokemon in self.selected_pokemon:
                        custom_widget.checkbox.setChecked(True)
                    list_item = QListWidgetItem(self.settingsPokemonListWidget)
                    list_item.setSizeHint(custom_widget.sizeHint())
                    self.settingsPokemonListWidget.addItem(list_item)
                    self.settingsPokemonListWidget.setItemWidget(list_item, custom_widget)

                # ------ MAIN POKEMON LOADING ------
                #get data from each mon in json
                if pokemon not in self.selected_pokemon:
                    continue
                num = data.get("num", -1)
                name = data.get("name", "")
                types = data.get("types", [])

                abilities = data.get("abilities", {}).items()
                base_abilities = []
                hidden_abilities = []
                for key, value in abilities:
                    if key == 'H':
                        hidden_abilities.append(value)
                    else:
                        base_abilities.append(value)

                stats = list(data.get("baseStats", {}).values())
                moves = learnset_data.get(pokemon, [])

                favourite = True if name in favourites.get("favourites") else False

                # update highest and lowest stats
                for i, stat in enumerate(stats):
                    if stat > self.highest_stats[i]:
                        self.highest_stats[i] = stat
                    if stat < self.lowest_stats[i]:
                        self.lowest_stats[i] = stat

                # create pokemon object
                pokemon_obj = PokemonData(
                    num=num,
                    name=name,
                    types=types,
                    base_abilities=base_abilities,
                    hidden_abilities=hidden_abilities,
                    stats=stats,
                    moves=moves,
                    favourite=favourite
                )

                # populate lists of pokemon
                self.master_list.append(pokemon_obj)
                self.filtered_sorted_list.append(pokemon_obj)

                # get lists of all possible moves, names, abilities
                self.all_names.append(name)
                abilities = data.get("abilities", {}).items()
                for _, value in abilities:
                    self.all_abilities.add(value)

            for moves in learnset_data.values():
                self.all_moves.update(moves)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    def initialise_completer(self):
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        #self.completer.activated.connect(self.add_to_applied_filters)
        self.completer.highlighted.connect(self.add_to_applied_filters)
        self.searchBar.setCompleter(self.completer)

    def initialise_connections(self):
        self.actionSettings.triggered.connect(lambda: self.toggle_settings(1))
        self.actionHelp.triggered.connect(self.show_help)
        self.backButton.clicked.connect(lambda: self.toggle_settings(0))

        # main page
        self.pokemonListWidget.itemClicked.connect(self.open_pokemon_popup)
        self.clearFiltersButton.clicked.connect(self.clear_filters)
        self.searchBar.textChanged.connect(self.filter_completer)
        self.nameLabel.clicked.connect(lambda: self.sort_by_trait("name"))
        self.hpLabel.clicked.connect(lambda: self.sort_by_trait("hp"))
        self.atkLabel.clicked.connect(lambda: self.sort_by_trait("atk"))
        self.defLabel.clicked.connect(lambda: self.sort_by_trait("def"))
        self.spaLabel.clicked.connect(lambda: self.sort_by_trait("spa"))
        self.spdLabel.clicked.connect(lambda: self.sort_by_trait("spd"))
        self.speLabel.clicked.connect(lambda: self.sort_by_trait("spe"))
        self.bstLabel.clicked.connect(lambda: self.sort_by_trait("bst"))

        # settings page
        self.applyButton.clicked.connect(self.apply_pokemon_list)
        self.exportPokemonButton.clicked.connect(self.export_pokemon_list)
        self.importPokemonButton.clicked.connect(self.import_pokemon_list)
        self.resetPokemonButton.clicked.connect(self.reset_pokemon_list)

    def initialise_spinner(self):
        sl = 100 # side length
        self.spinner_label = QLabel(self)
        self.spinner_label.setFixedSize(sl, sl) # spinner gif is 200 by 200 pixels
        self.spinner_label.setStyleSheet("background-color: transparent;")
        self.spinner_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.spinner_label.setVisible(False)

        spinner_path = os.path.join("assets", "loading", "spinner.gif")
        self.spinner_movie = QMovie(spinner_path)
        self.spinner_movie.setScaledSize(QSize(sl, sl))
        self.spinner_label.setMovie(self.spinner_movie)

        self.spinner_label.move(max(0, self.width() / 2 - sl/2), max(0, self.height() / 2 - sl/2))

    def toggle_settings(self, i):
        self.stackedWidget.setCurrentIndex(i)

    def show_help(self):
        """Shows a help dialog with instructions on how to use the app."""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Help")
        layout = QVBoxLayout(help_dialog)

        instructions = (
            "Developed by elliottsneath\n"
            "    discord: vapelordell\n\n"
            "Welcome to the Pokémon Searcher!\n\n"
            "To choose a selection of pokémon, visit the settings page, and either \n"
            "manually select pokémon from the list, or import a list of pokémon from a file."
            "This includes using a .pkmlist file or a TomSprite Google Sheet.\n"
            "If you wish to make your own google sheet, select the pokémon you want, and\n"
            "export as a google sheet."
        )

        label = QLabel(instructions)
        layout.addWidget(label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(help_dialog.close)
        layout.addWidget(close_button)

        help_dialog.exec()

    def apply_pokemon_list(self, popup = True):
        """Applies the current filtered pokemon list to the main page."""
        if popup:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Confirm Apply")
            msg.setText("Are you sure you want to apply the changes to the Pokémon list?")
            msg.setInformativeText("This will overwrite the selected Pokémon list and changes will remain after restarting the app.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            result = msg.exec()
            if result == QMessageBox.Cancel:
                return
        
        self.master_list = []
        self.filtered_sorted_list = []
        self.applied_filters = []
        self.selected_trait = None
        self.trait_reverse = True
        self.selected_pokemon = []

        for i in range(self.settingsPokemonListWidget.count()):
            item = self.settingsPokemonListWidget.item(i)
            widget = self.settingsPokemonListWidget.itemWidget(item)
            widget:SettingsPokemonListItem
            if widget.checkbox.isChecked():
                name = widget.name_label.text()
                self.selected_pokemon.append(name)

        try:
            with open(SELECTED_POKEMON_PATH, "w") as f:
                json.dump({"selected_pokemon": self.selected_pokemon}, f, indent=4)
        except Exception as e:
            print(f"Error saving selected Pokémon: {e}")

        self.load_pokemon_data(False)
        self.update_filtered_pokemon()

    def export_pokemon_list(self):
        """Exports current filtered pokemon list to a custom file type (.pkmnlist)."""
        self.apply_pokemon_list(False)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Pokémon List",
            "",
            "Pokémon List Files (*.pkmnlist);;JSON Files (*.json);;All Files (*)",
            options=options
        )
        if not file_path:
            return

        if not file_path.endswith(".pkmnlist"):
            file_path += ".pkmnlist"

        try:
            with open(file_path, "w") as f:
                json.dump({"selected_pokemon": self.selected_pokemon}, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export Pokémon list:\n{e}")

    def import_pokemon_list(self):
        """Opens a popup for importing Pokémon list via text, file, or Google Sheet."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Import Pokémon List")
        layout = QVBoxLayout(dialog)

        label = QLabel("Paste a comma-separated list of Pokémon names below:")
        layout.addWidget(label)

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        file_button = QPushButton("Import from File")
        google_button = QPushButton("Import from Google Sheet")
        apply_button = QPushButton("Apply List")
        button_layout.addWidget(file_button)
        button_layout.addWidget(google_button)
        button_layout.addWidget(apply_button)

        self.master_list = []
        self.filtered_sorted_list = []
        self.applied_filters = []
        self.selected_trait = None
        self.trait_reverse = True
        self.selected_pokemon = []

        def import_from_file():
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Pokémon List",
                "",
                "Pokémon List Files (*.pkmnlist);;JSON Files (*.json);;All Files (*)",
                options=options
            )
            if not file_path:
                return
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                selected = data.get("selected_pokemon")
                if not isinstance(selected, list):
                    raise ValueError("Invalid file format: 'selected_pokemon' not found or not a list.")
                
                self.selected_pokemon = selected
                for widget in self.settingsPokemonListWidget.findChildren(SettingsPokemonListItem):
                    if widget.name_label.text() in self.selected_pokemon:
                        widget.checkbox.setChecked(True)
                    else:
                        widget.checkbox.setChecked(False)

                with open(SELECTED_POKEMON_PATH, "w") as f:
                    json.dump({"selected_pokemon": self.selected_pokemon}, f, indent=4)

                self.load_pokemon_data(False)
                self.update_filtered_pokemon()
                QMessageBox.information(self, "Import Successful", "Pokémon list imported successfully.")
                dialog.accept()

            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import Pokémon list:\n{e}")

        def import_from_text():
            text = text_edit.toPlainText()
            names = [name.strip() for name in text.split(",") if name.strip()]
            if not names:
                QMessageBox.warning(self, "Input Error", "Please enter at least one Pokémon name.")
                return
            self.selected_pokemon = names
            with open(SELECTED_POKEMON_PATH, "w") as f:
                json.dump({"selected_pokemon": self.selected_pokemon}, f, indent=4)
            self.load_pokemon_data(False)
            self.update_filtered_pokemon()
            QMessageBox.information(self, "Import Successful", "Pokémon list imported successfully.")
            dialog.accept()

        def import_from_google():
            QMessageBox.information(self, "Coming Soon", "Google Sheets import will be implemented later.")

        file_button.clicked.connect(import_from_file)
        google_button.clicked.connect(import_from_google)
        apply_button.clicked.connect(import_from_text)

        dialog.exec()

    def reset_pokemon_list(self):
        """Resets the filtered pokemon list to the original pokedex"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirm Reset")
        msg.setText("Are you sure you want to reset the Pokémon list?")
        msg.setInformativeText("This will clear any previous selections and mark the entire Pokédex as available.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        result = msg.exec()
        if result == QMessageBox.Cancel:
            return
        
        for i in range(self.settingsPokemonListWidget.count()):
            item = self.settingsPokemonListWidget.item(i)
            widget = self.settingsPokemonListWidget.itemWidget(item)
            if widget and hasattr(widget, "checkbox"):
                widget.checkbox.setChecked(True)

        self.master_list = []
        self.filtered_sorted_list = []
        self.applied_filters = []
        self.selected_trait = None
        self.trait_reverse = True

        self.selected_pokemon = [name for name in self.pokedex]

        try:
            with open(SELECTED_POKEMON_PATH, "w") as f:
                json.dump({"selected_pokemon": self.selected_pokemon}, f, indent=4)
        except Exception as e:
            print(f"Error saving selected Pokémon: {e}")

        self.load_pokemon_data(False)
        self.update_filtered_pokemon()

    def add_to_applied_filters(self, selected_item):
        keyword, category = selected_item.split(" - ")
        keyword = keyword.strip().lower()
        category = category.strip().lower()
        self.applied_filters.append((keyword, category))

        self.add_filter_to_ui(selected_item)
        self.update_filtered_pokemon()

    def add_filter_to_ui(self, selected_item):
        filter_widget = QWidget(self)
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(2, 2, 2, 2)
        filter_layout.setSpacing(5)
        filter_layout.setAlignment(Qt.AlignLeft)

        filter_label = QLabel(selected_item, filter_widget)
        filter_label.setStyleSheet(
            """
            color: black;
            font-size: 10px;
            background-color: rgba(211, 211, 211, 0.8);
            border-radius: 5px;
            padding: 2px;
            """
        )
        filter_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        filter_layout.addWidget(filter_label)

        remove_label = QLabel(filter_widget)
        remove_label.setText("X")
        remove_label.setAlignment(Qt.AlignCenter)
        remove_label.setStyleSheet(
            """
            color: rgba(211, 211, 211, 0.8);
            background-color: rgba(255, 0, 0, 0.2);
            border-radius: 8px;
            font-size: 10px;
            width: 16px;
            height: 16px;
            """
        )
        remove_label.setFixedSize(16, 16)
        filter_layout.addWidget(remove_label)
        spacer_index = self.filterLayout.count() - 1
        self.filterLayout.insertWidget(spacer_index, filter_widget)

        remove_label.mousePressEvent = lambda event: self.remove_filter(filter_widget, selected_item)

        QTimer.singleShot(10, lambda: self.searchBar.setText(""))

    def remove_filter(self, filter_widget, selected_item):
        keyword, category = selected_item.split(" - ")
        keyword = keyword.strip().lower()
        category = category.strip().lower()
        if (keyword, category) in self.applied_filters:
            self.applied_filters.remove((keyword, category))

        self.filterLayout.removeWidget(filter_widget)
        filter_widget.deleteLater()

        self.update_filtered_pokemon()

    def clear_filters(self):
        self.applied_filters = []
        self.update_filtered_pokemon()

    def sort_by_trait(self, trait):
        label: ClickableLabel = getattr(self, f"{trait}Label")

        if self.selected_trait == None:
            label.highlight(True)
            self.selected_trait = trait
            self.trait_reverse = True

        elif self.selected_trait == trait:
            if self.trait_reverse == False:
                label.highlight(False)
                self.selected_trait = None
                self.trait_reverse = True
            else:
                self.trait_reverse = False
        
        else:
            label.highlight(True)
            prev_label: ClickableLabel = getattr(self, f"{self.selected_trait}Label")
            prev_label.highlight(False)
            self.selected_trait = trait
            self.trait_reverse = True

        self.update_filtered_pokemon()

    def update_filtered_pokemon(self):
        self.filtered_sorted_list = []
        # filter first then sort, so we are sorting with less
        for pokemon in self.master_list:
            if self.applied_filters == []:
                self.filtered_sorted_list = self.master_list
                break

            pokemon: PokemonData
            matches_filter = True
            for keyword, category in self.applied_filters:
                if category == "pokemon" and keyword not in pokemon.name.lower():
                    matches_filter = False
                elif category == "type" and keyword not in [t.lower() for t in pokemon.types]:
                    matches_filter = False
                elif category == "ability" and keyword not in [a.lower() for a in pokemon.base_abilities + pokemon.hidden_abilities]:
                    matches_filter = False
                elif category == "move" and keyword not in [m.lower() for m in pokemon.moves]:
                    matches_filter = False

            if matches_filter:
                self.filtered_sorted_list.append(pokemon)

        # now we have all filtered pokemon in self.filtered_sorted_list
        if self.selected_trait == None or self.selected_trait == "num":
            sort_key = lambda pokemon: pokemon.num
            reverse = not self.trait_reverse
        elif self.selected_trait == "name":
            sort_key = lambda pokemon: pokemon.name
            reverse = not self.trait_reverse
        elif self.selected_trait == "bst":
            sort_key = lambda pokemon: sum(pokemon.stats)
            reverse = self.trait_reverse 
        else:
            stats = ["hp","atk","def","spa","spd","spe"]
            sort_key = lambda pokemon: pokemon.stats[stats.index(self.selected_trait)]
            reverse = self.trait_reverse

        self.filtered_sorted_list = sorted(self.filtered_sorted_list, key=sort_key, reverse=reverse)
        self.filtered_sorted_list = [p for p in self.filtered_sorted_list if p.favourite] + [p for p in self.filtered_sorted_list if not p.favourite]
        
        self.update_pokemon_list_ui()

    def show_spinner(self):
        self.spinner_label.setVisible(True)
        self.spinner_movie.start()
        QApplication.processEvents()

    def hide_spinner(self):
        self.spinner_movie.stop()
        self.spinner_label.setVisible(False)

    def update_pokemon_list_ui(self):
        self.pokemonListWidget.clear()
        self.list_build_index = 0
        self.list_build_batch_size = 10

        self.show_spinner()
        self._build_pokemon_list_batch()

    def _build_pokemon_list_batch(self):
        start = self.list_build_index
        end = start + self.list_build_batch_size
        subset = self.filtered_sorted_list[start:end]

        for pokemon in subset:
            custom_widget = PokemonListItem(pokemon)
            list_item = QListWidgetItem(self.pokemonListWidget)
            list_item.setSizeHint(custom_widget.sizeHint())
            self.pokemonListWidget.addItem(list_item)
            self.pokemonListWidget.setItemWidget(list_item, custom_widget)

        self.list_build_index = end
        if self.list_build_index < len(self.filtered_sorted_list):
            QTimer.singleShot(0, self._build_pokemon_list_batch)
        else:
            self.hide_spinner()

    def filter_completer(self, text: str):
        def get_filtered_list(items, label):
            return [f"{item} - {label}" for item in items]

        filter_list = []

        if self.pokemonCheckbox.isChecked():
            filter_list += get_filtered_list(self.all_names, "Pokemon")

        if self.movesCheckbox.isChecked():
            filter_list += get_filtered_list(self.all_moves, "Move")

        if self.typesCheckbox.isChecked():
            filter_list += get_filtered_list(self.all_types, "Type")

        if self.abilitiesCheckbox.isChecked():
            filter_list += get_filtered_list(self.all_abilities, "Ability")

        if not filter_list:
            filter_list = (
                get_filtered_list(self.all_names, "Pokemon")
                + get_filtered_list(self.all_moves, "Move")
                + get_filtered_list(self.all_types, "Type")
                + get_filtered_list(self.all_abilities, "Ability")
            )

        refined_list = [item for item in filter_list if text.lower() in item.lower()]

        self.completer.setModel(QStringListModel(refined_list))

    def open_pokemon_popup(self, item):
        index = self.pokemonListWidget.row(item)
        selected_pokemon = self.filtered_sorted_list[index]

        self.popup = QDialog(self)
        self.ui = Ui_PokemonPopup()
        self.ui.setupUi(self.popup)

        self.ui.lineEdit.textChanged.connect(lambda text: self.update_moves_in_popup(text, selected_pokemon))
        self.ui.starLabel.clicked.connect(lambda: self.update_favourites(selected_pokemon))

        self.ui.nameLabel.setText(selected_pokemon.name)
        
        star_png = "star_filled.png" if selected_pokemon.favourite else "star.png"
        png_path = os.path.join("assets", "icons", star_png)
        self.ui.starLabel.setPixmap(QPixmap(png_path).scaled(36, 36))
        
        if len(selected_pokemon.types) < 2:
            type = selected_pokemon.types[0]
            svg_path = os.path.join("assets", "icons", f"{type.lower()}.svg")
            pixmap = QPixmap(svg_path)
            if not pixmap.isNull():
                self.ui.type1Label.setPixmap(pixmap.scaled(36, 36))
                self.ui.type2Label.setText("")
            else:
                self.ui.type1Label.setText(type)
                self.ui.type2Label.setText("")
        else:
            type1 = selected_pokemon.types[0]
            type2 = selected_pokemon.types[1]
            svg_path1 = os.path.join("assets", "icons", f"{type1.lower()}.svg")
            svg_path2 = os.path.join("assets", "icons", f"{type2.lower()}.svg")
            pixmap1 = QPixmap(svg_path1)
            pixmap2 = QPixmap(svg_path2)
            if not pixmap1.isNull() and not pixmap2.isNull():
                self.ui.type1Label.setPixmap(pixmap1.scaled(36, 36))
                self.ui.type2Label.setPixmap(pixmap2.scaled(36, 36))
            else:
                self.ui.type1Label.setText(type1)
                self.ui.type2Label.setText(type2)

        stats = selected_pokemon.stats

        self.ui.hpNumLabel.setText(str(stats[0]))
        self.ui.atkNumLabel.setText(str(stats[1]))
        self.ui.defNumLabel.setText(str(stats[2]))
        self.ui.spaNumLabel.setText(str(stats[3]))
        self.ui.spdNumLabel.setText(str(stats[4]))
        self.ui.speNumLabel.setText(str(stats[5]))

        stat_bars = [
            self.ui.hpStatBar,
            self.ui.atkStatBar,
            self.ui.defStatBar,
            self.ui.spaStatBar,
            self.ui.spdStatBar,
            self.ui.speStatBar,
        ]

        for i, stat in enumerate(stats):
            lowest = self.lowest_stats[i]
            highest = self.highest_stats[i]

            normalized_value = (stat - lowest) / (highest - lowest) if highest > lowest else 0

            red = int(255 * (1 - normalized_value))
            green = int(255 * normalized_value)
            color = QColor(red, green, 0)

            stat_bars[i].set_value(stat, max_stat=highest)
            stat_bars[i].color = color
            stat_bars[i].update()

        self.ui.moveListWidget.clear()
        for move in selected_pokemon.moves:
            self.ui.moveListWidget.addItem(move)

        self.popup.exec()

    def update_favourites(self, pokemon):
        pokemon.favourite = not pokemon.favourite
        self.ui.starLabel.change_star(pokemon.favourite)
        self.update_filtered_pokemon()

    def update_moves_in_popup(self, text: str, selected_pokemon):
        self.ui.moveListWidget.clear()
        for move in selected_pokemon.moves:
            if text in move:
                self.ui.moveListWidget.addItem(move)

    def closeEvent(self, event):
        try:
            favourite_names = [pokemon.name for pokemon in self.master_list if pokemon.favourite]

            with open(CONFIG_FILE_PATH, 'w') as f:
                json.dump({"favourites": favourite_names}, f, indent=4)

            print("Favourites saved successfully.")
        except Exception as e:
            print(f"Error saving favourites: {e}")

        event.accept()
        

def handle_exception(exc_type, exc_value, exc_traceback):
    import traceback
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print("=====================================================")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print("=====================================================")

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icons/JCB_Logo'))

    icon = QPixmap('assets/icons/JCB_Logo')
    resized_icon = icon.scaled(icon.size() * 0.5, Qt.KeepAspectRatio)

    spl = QSplashScreen(resized_icon)
    spl.show()
    spl.activateWindow()

    window = MainWindow()
    window.loaded.connect(lambda: spl.finish(window))
    window.show()
    spl.finish(window)

    sys.exit(app.exec())

if __name__ == '__main__':
    sys.excepthook = handle_exception
    main()