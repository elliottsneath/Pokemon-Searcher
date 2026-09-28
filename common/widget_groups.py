"""Widget group dataclasses: typed bundles of Qt widgets passed to plot handlers and persistence mixins."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow

class MainWidgets:
    def __init__(self, w: MainWindow):
        self.search_bar = w.searchBar
        self.clear_filters_button = w.clearFiltersButton
        self.filter_layout = w.filterLayout
        self.pokemon_checkbox = w.pokemonCheckbox
        self.type_checkbox = w.typesCheckbox
        self.ability_checkbox = w.abilitiesCheckbox
        self.move_checkbox = w.movesCheckbox
        self.hide_drafted_checkbox = w.hideDraftedCheckbox
        self.pokemon_list_widget = w.pokemonListWidget
        self.sort_labels = {
            "name": w.nameLabel,
            "hp":   w.hpLabel,
            "atk":  w.atkLabel,
            "def":  w.defLabel,
            "spa":  w.spaLabel,
            "spd":  w.spdLabel,
            "spe":  w.speLabel,
            "bst":  w.bstLabel,
            "cost": w.costLabel,
        }

class SettingsWidgets:
    def __init__(self, w: MainWindow):
        self.apply_button = w.applyButton
        self.export_button = w.exportPokemonButton
        self.import_button = w.importPokemonButton
        self.back_button = w.backButton
        self.search_bar = w.settingsSearchBar
        self.pool_combo = w.poolComboBox
        self.reset_button = w.resetPokemonButton
        self.pokemon_list_widget = w.settingsPokemonListWidget
