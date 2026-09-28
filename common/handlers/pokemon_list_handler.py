"""Handles the main Pokémon list: filtering, sorting, rendering, completer, spinner, and popup."""

from __future__ import annotations
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QApplication, QCompleter, QDialog, QHBoxLayout, QLabel,
    QListWidgetItem, QSizePolicy, QWidget,
)
from PySide6.QtGui import QColor, QMovie, QPixmap, Qt
from PySide6.QtCore import QSize, QStringListModel, QTimer

from assets.ui.pokemon_list_item import PokemonListItem
from assets.ui.pokemon_popup_ui import Ui_PokemonPopup
from common.widget_groups import MainWidgets
from data.pokemon_obj import PokemonData

if TYPE_CHECKING:
    from main import MainWindow


class PokemonListHandler:
    def __init__(self, window: MainWindow, widgets: MainWidgets):
        self.w = window
        self.wg = widgets

        self.filtered_sorted_list: list[PokemonData] = []
        self.applied_filters: list[tuple[str, str]] = []
        self.selected_trait: str | None = None
        self.trait_reverse: bool = True

        self._build_index = 0
        self._build_batch_size = 10

        self._init_completer()
        self._init_spinner()
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.wg.pokemon_list_widget.itemClicked.connect(self.open_pokemon_popup)
        self.wg.clear_filters_button.clicked.connect(self.clear_filters)
        self.wg.pokemon_checkbox.stateChanged.connect(self.filter_completer)
        self.wg.move_checkbox.stateChanged.connect(self.filter_completer)
        self.wg.type_checkbox.stateChanged.connect(self.filter_completer)
        self.wg.ability_checkbox.stateChanged.connect(self.filter_completer)
        self.wg.hide_drafted_checkbox.setChecked(self.w.hide_drafted)
        self.wg.hide_drafted_checkbox.stateChanged.connect(self._toggle_hide_drafted)
        for trait, label in self.wg.sort_labels.items():
            label.clicked.connect(lambda t=trait: self.sort_by_trait(t))

    # ── hide drafted ───────────────────────────────────────────────────────

    def _toggle_hide_drafted(self) -> None:
        self.w.hide_drafted = self.wg.hide_drafted_checkbox.isChecked()
        self.w.data_handler.save_config()
        self.update()

    # ── public reset ───────────────────────────────────────────────────────

    def reset_state(self) -> None:
        self.filtered_sorted_list = []
        self.applied_filters = []
        self.selected_trait = None
        self.trait_reverse = True

    # ── filtering / sorting ────────────────────────────────────────────────

    def update(self) -> None:
        self.filtered_sorted_list = []
        for pokemon in self.w.master_list:
            if not self.applied_filters:
                self.filtered_sorted_list = list(self.w.master_list)
                break
            if self._matches(pokemon):
                self.filtered_sorted_list.append(pokemon)

        if self.w.hide_drafted:
            self.filtered_sorted_list = [p for p in self.filtered_sorted_list if not p.drafted]

        self.filtered_sorted_list.sort(key=self._sort_key(), reverse=self._sort_reverse())
        self.filtered_sorted_list = (
            [p for p in self.filtered_sorted_list if p.favourite] +
            [p for p in self.filtered_sorted_list if not p.favourite]
        )
        self._rebuild_list_ui()

    def _matches(self, pokemon: PokemonData) -> bool:
        for keyword, category in self.applied_filters:
            if category == "pokemon" and keyword not in pokemon.name.lower():
                return False
            if category == "type" and keyword not in [t.lower() for t in pokemon.types]:
                return False
            if category == "ability" and keyword not in [a.lower() for a in pokemon.base_abilities + pokemon.hidden_abilities]:
                return False
            if category == "move" and keyword not in [m.lower() for m in pokemon.moves]:
                return False
        return True

    def _sort_key(self):
        t = self.selected_trait
        if t is None or t == "num": return lambda p: p.num
        if t == "name":             return lambda p: p.name
        if t == "bst":              return lambda p: sum(p.stats)
        if t == "cost":             return lambda p: p.cost if p.cost is not None else -1
        idx = ["hp", "atk", "def", "spa", "spd", "spe"].index(t)
        return lambda p: p.stats[idx]

    def _sort_reverse(self) -> bool:
        t = self.selected_trait
        return not self.trait_reverse if (t is None or t in ("num", "name")) else self.trait_reverse

    def sort_by_trait(self, trait: str) -> None:
        label = self.wg.sort_labels[trait]
        if self.selected_trait is None:
            label.highlight(True)
            self.selected_trait = trait
            self.trait_reverse = True
        elif self.selected_trait == trait:
            if not self.trait_reverse:
                label.highlight(False)
                self.selected_trait = None
                self.trait_reverse = True
            else:
                self.trait_reverse = False
        else:
            label.highlight(True)
            self.wg.sort_labels[self.selected_trait].highlight(False)
            self.selected_trait = trait
            self.trait_reverse = True
        self.update()

    # ── filter chips ───────────────────────────────────────────────────────

    def add_to_applied_filters(self, selected_item: str) -> None:
        keyword, category = selected_item.split(" - ")
        self.applied_filters.append((keyword.strip().lower(), category.strip().lower()))
        self._add_filter_chip(selected_item)
        self.update()
        QTimer.singleShot(0, self.wg.search_bar.clear)

    def _add_filter_chip(self, selected_item: str) -> None:
        chip = QWidget()
        layout = QHBoxLayout(chip)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignLeft)

        lbl = QLabel(selected_item, chip)
        lbl.setStyleSheet(
            "color:black;font-size:10px;"
            "background-color:rgba(211,211,211,0.8);"
            "border-radius:5px;padding:2px;"
        )
        lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addWidget(lbl)

        x_btn = QLabel("X", chip)
        x_btn.setAlignment(Qt.AlignCenter)
        x_btn.setStyleSheet(
            "color:rgba(211,211,211,0.8);"
            "background-color:rgba(255,0,0,0.2);"
            "border-radius:8px;font-size:10px;"
            "width:16px;height:16px;"
        )
        x_btn.setFixedSize(16, 16)
        layout.addWidget(x_btn)

        idx = self.wg.filter_layout.count() - 1
        self.wg.filter_layout.insertWidget(idx, chip)
        x_btn.mousePressEvent = lambda _: self.remove_filter(chip, selected_item)

    def remove_filter(self, chip: QWidget, selected_item: str) -> None:
        keyword, category = selected_item.split(" - ")
        pair = (keyword.strip().lower(), category.strip().lower())
        if pair in self.applied_filters:
            self.applied_filters.remove(pair)
        self.wg.filter_layout.removeWidget(chip)
        chip.deleteLater()
        self.update()

    def clear_filters(self) -> None:
        self.applied_filters = []
        self.update()

    # ── completer ──────────────────────────────────────────────────────────

    def _init_completer(self) -> None:
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.activated.connect(self.add_to_applied_filters)
        self.wg.search_bar.setCompleter(self.completer)
        self.filter_completer()

    def filter_completer(self) -> None:
        def tagged(items, tag): return [f"{i} - {tag}" for i in items]
        items = []
        if self.wg.pokemon_checkbox.isChecked():  items += tagged(self.w.all_names, "Pokemon")
        if self.wg.move_checkbox.isChecked():      items += tagged(self.w.all_moves, "Move")
        if self.wg.type_checkbox.isChecked():      items += tagged(self.w.all_types, "Type")
        if self.wg.ability_checkbox.isChecked():   items += tagged(self.w.all_abilities, "Ability")
        if not items:
            items = (tagged(self.w.all_names, "Pokemon") + tagged(self.w.all_moves, "Move") +
                     tagged(self.w.all_types, "Type") + tagged(self.w.all_abilities, "Ability"))
        self.completer.setModel(QStringListModel(items))

    # ── list rendering ─────────────────────────────────────────────────────

    def _rebuild_list_ui(self) -> None:
        self.wg.pokemon_list_widget.clear()
        self._build_index = 0
        self._show_spinner()
        self._build_batch()

    def _build_batch(self) -> None:
        subset = self.filtered_sorted_list[self._build_index:self._build_index + self._build_batch_size]
        for pokemon in subset:
            widget = PokemonListItem(pokemon)
            item = QListWidgetItem(self.wg.pokemon_list_widget)
            item.setSizeHint(widget.sizeHint())
            self.wg.pokemon_list_widget.addItem(item)
            self.wg.pokemon_list_widget.setItemWidget(item, widget)
        self._build_index += self._build_batch_size
        if self._build_index < len(self.filtered_sorted_list):
            QTimer.singleShot(0, self._build_batch)
        else:
            self._hide_spinner()

    # ── popup ──────────────────────────────────────────────────────────────

    def open_pokemon_popup(self, item) -> None:
        pokemon = self.filtered_sorted_list[self.wg.pokemon_list_widget.row(item)]

        self._popup_dialog = QDialog(self.w)
        self._popup_ui = Ui_PokemonPopup()
        self._popup_ui.setupUi(self._popup_dialog)
        ui = self._popup_ui

        ui.lineEdit.textChanged.connect(lambda text: self._filter_moves(text, pokemon))
        ui.starLabel.clicked.connect(lambda: self._toggle_favourite(pokemon))

        title = pokemon.name
        if pokemon.cost is not None:
            title += f" ({pokemon.cost} pts)"
        if pokemon.drafted:
            title += " - Drafted"
        ui.nameLabel.setText(title)

        star = "star_filled.png" if pokemon.favourite else "star.png"
        ui.starLabel.setPixmap(QPixmap(os.path.join("assets", "icons", star)).scaled(36, 36))

        types = pokemon.types
        if len(types) < 2:
            pix = QPixmap(os.path.join("assets", "icons", f"{types[0].lower()}.svg"))
            (ui.type1Label.setPixmap(pix.scaled(36, 36)) if not pix.isNull() else ui.type1Label.setText(types[0]))
            ui.type2Label.setText("")
        else:
            for attr, t in [("type1Label", types[0]), ("type2Label", types[1])]:
                pix = QPixmap(os.path.join("assets", "icons", f"{t.lower()}.svg"))
                lbl = getattr(ui, attr)
                lbl.setPixmap(pix.scaled(36, 36)) if not pix.isNull() else lbl.setText(t)

        num_labels = ["hpNumLabel", "atkNumLabel", "defNumLabel", "spaNumLabel", "spdNumLabel", "speNumLabel"]
        stat_bars  = [ui.hpStatBar, ui.atkStatBar, ui.defStatBar, ui.spaStatBar, ui.spdStatBar, ui.speStatBar]
        for i, stat in enumerate(pokemon.stats):
            getattr(ui, num_labels[i]).setText(str(stat))
            lo, hi = self.w.lowest_stats[i], self.w.highest_stats[i]
            norm = (stat - lo) / (hi - lo) if hi > lo else 0
            stat_bars[i].color = QColor(int(255 * (1 - norm)), int(255 * norm), 0)
            stat_bars[i].set_value(stat, max_stat=hi)
            stat_bars[i].update()

        ui.moveListWidget.clear()
        for move in pokemon.moves:
            ui.moveListWidget.addItem(move)

        self._popup_dialog.exec()

    def _toggle_favourite(self, pokemon: PokemonData) -> None:
        pokemon.favourite = not pokemon.favourite
        self._popup_ui.starLabel.change_star(pokemon.favourite)
        self.update()

    def _filter_moves(self, text: str, pokemon: PokemonData) -> None:
        self._popup_ui.moveListWidget.clear()
        for move in pokemon.moves:
            if text in move:
                self._popup_ui.moveListWidget.addItem(move)

    # ── spinner ────────────────────────────────────────────────────────────

    def _init_spinner(self) -> None:
        sl = 250
        self._spinner_label = QLabel(self.w)
        self._spinner_label.setFixedSize(sl, sl)
        self._spinner_label.setStyleSheet("background-color: transparent;")
        self._spinner_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._spinner_label.setVisible(False)
        self._spinner_movie = QMovie(os.path.join("assets", "loading", "loading.gif"))
        self._spinner_movie.setScaledSize(QSize(sl, sl))
        self._spinner_label.setMovie(self._spinner_movie)
        self._spinner_label.move(
            max(0, int(self.w.width() / 2 - sl / 2)),
            max(0, int(self.w.height() / 2 - sl / 2)),
        )

    def _show_spinner(self) -> None:
        self._spinner_label.setVisible(True)
        self._spinner_movie.start()
        QApplication.processEvents()

    def _hide_spinner(self) -> None:
        self._spinner_movie.stop()
        self._spinner_label.setVisible(False)
