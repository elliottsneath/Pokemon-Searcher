"""Widget group dataclasses: typed bundles of Qt widgets passed to plot handlers and persistence mixins."""

from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLabel, QWidget

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

class PickSlot:
    __slots__ = ("widget", "sprite", "name", "type_widget", "pts")
    def __init__(self, widget: QWidget, sprite: QLabel, name: QLabel, type_widget: QWidget, pts: QLabel):
        self.widget = widget
        self.sprite = sprite
        self.name = name
        self.type_widget = type_widget
        self.pts = pts

class DraftHandlerWidgets:
    def __init__(self, w: MainWindow):
        self.action = w.actionCurrentDraft

        self.picks_label = w.picksLabel
        self.pts_label = w.ptsLabel
        self.refresh_label = w.importLabel

        self.picks = [
            PickSlot(
                getattr(w, f"pick_{i:02d}_widget"),
                getattr(w, f"pick_{i:02d}_sprite"),
                getattr(w, f"pick_{i:02d}_name"),
                getattr(w, f"pick_{i:02d}_type"),
                getattr(w, f"pick_{i:02d}_pts"),
            )
            for i in range(1, 13)
        ]

        self.weaknesses_widget = w.widget_17
        self.resistances_widget = w.widget_18
        self.immunities_widget = w.widget_19
        self.recommendations_widget = w.recommendationsFrame
        self.budget_line_edit = w.budgetLineEdit

class SettingsWidgets:
    def __init__(self, w: MainWindow):
        self.pool_combo = w.poolComboBox
        self.budget_line_edit = w.budgetLineEdit
        self.apply_button = w.applyButton
        self.export_button = w.exportPokemonButton
        self.import_button = w.importPokemonButton
        self.search_bar = w.settingsSearchBar
        self.reset_button = w.resetPokemonButton
        self.pokemon_list_widget = w.settingsPokemonListWidget

        self.budget_line_edit.setValidator(QIntValidator(0, 999))
