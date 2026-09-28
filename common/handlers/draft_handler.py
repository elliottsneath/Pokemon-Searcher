from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel

from common.paths import DRAFT_STATE_PATH
from common.sprite_loader import get_sprite
from common.widget_groups import DraftHandlerWidgets, PickSlot
from data.pokemon_obj import PokemonData

if TYPE_CHECKING:
    from main import MainWindow


class DraftHandler:
    def __init__(self, window: MainWindow, widgets: DraftHandlerWidgets):
        self.w = window
        self.wg = widgets
        self.drafted_pokemon: list[PokemonData | None] = [None] * 12
        for i, slot in enumerate(self.wg.picks):
            slot.name.setAlignment(Qt.AlignCenter)
            slot.name.setText(f"Pick {i + 1}")
            slot.widget.setStyleSheet(
                f"QWidget#{slot.widget.objectName()} {{ border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; }}"
            )
            slot.widget.mousePressEvent = self._make_slot_click_handler(i)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.wg.budget_line_edit.textChanged.connect(self.update_budget)
        self._load_draft_state()

    # ── public ────────────────────────────────────────────────────────────────

    def is_drafted(self, pokemon: PokemonData) -> bool:
        return pokemon in self.drafted_pokemon

    def add_to_draft(self, pokemon: PokemonData) -> None:
        idx = self.get_next_blank()
        if idx is None:
            return
        self.drafted_pokemon[idx] = pokemon
        self._populate_slot(self.wg.picks[idx], pokemon)
        self.update_budget()
        self.update_picks_label()

    def remove_from_draft(self, pokemon: PokemonData) -> None:
        try:
            idx = self.drafted_pokemon.index(pokemon)
        except ValueError:
            return
        self.drafted_pokemon[idx] = None
        self._clear_slot(self.wg.picks[idx], idx)
        self.update_budget()
        self.update_picks_label()

    def update_budget(self) -> None:
        text = self.wg.budget_line_edit.text()
        budget = int(text) if text else 0
        spent = sum(p.cost for p in self.drafted_pokemon if p is not None and p.cost is not None)
        self.wg.pts_label.setText(f"{budget - spent} Pts Remaining")
        self._save_draft_state()

    def _save_draft_state(self) -> None:
        try:
            with open(DRAFT_STATE_PATH, "w") as f:
                json.dump({
                    "drafted": [p.species_id if p is not None else None for p in self.drafted_pokemon],
                    "budget": self.wg.budget_line_edit.text(),
                }, f, indent=4)
        except Exception as e:
            print(f"Draft state save failed: {e}")

    def _load_draft_state(self) -> None:
        if not os.path.exists(DRAFT_STATE_PATH):
            return
        try:
            with open(DRAFT_STATE_PATH) as f:
                data = json.load(f)
            species_map = {p.species_id: p for p in self.w.master_list}
            for i, sid in enumerate(data.get("drafted", [])):
                if sid and sid in species_map:
                    self.drafted_pokemon[i] = species_map[sid]
                    self._populate_slot(self.wg.picks[i], species_map[sid])
            if budget := data.get("budget"):
                self.wg.budget_line_edit.setText(str(budget))
            self.update_picks_label()
        except Exception as e:
            print(f"Draft state load failed: {e}")

    def update_picks_label(self) -> None:
        count = sum(1 for p in self.drafted_pokemon if p is not None)
        self.wg.picks_label.setText(f"{count}/12 Picks")

    def _make_slot_click_handler(self, idx: int):
        def handler(_):
            pokemon = self.drafted_pokemon[idx]
            if pokemon is not None:
                self.w.pokemon_list_handler.open_popup(pokemon)
        return handler

    def get_next_blank(self) -> int | None:
        for i, p in enumerate(self.drafted_pokemon):
            if p is None:
                return i
        return None

    # ── slot rendering ────────────────────────────────────────────────────────

    def _populate_slot(self, slot: PickSlot, pokemon: PokemonData) -> None:
        sprite = get_sprite(pokemon.species_id, pokemon.name)
        if sprite:
            slot.sprite.setPixmap(sprite.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            slot.sprite.setAlignment(Qt.AlignCenter)

        slot.name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = slot.name.font()
        font.setBold(True)
        slot.name.setFont(font)
        slot.name.setText(pokemon.name)
        slot.pts.setText(f"{pokemon.cost} pts" if pokemon.cost is not None else "")

        self._set_type_icons(slot, pokemon.types)

    def _clear_slot(self, slot: PickSlot, idx: int) -> None:
        slot.sprite.clear()
        slot.name.setAlignment(Qt.AlignCenter)
        font = slot.name.font()
        font.setBold(False)
        slot.name.setFont(font)
        slot.name.setText(f"Pick {idx + 1}")
        slot.pts.setText("")
        self._set_type_icons(slot, [])

    def _set_type_icons(self, slot: PickSlot, types: list[str]) -> None:
        layout = slot.type_widget.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for t in types:
            lbl = QLabel()
            pix = QPixmap(os.path.join("assets", "icons", f"{t.lower()}.svg"))
            if not pix.isNull():
                lbl.setPixmap(pix.scaled(24, 24))
            else:
                lbl.setText(t)
            layout.addWidget(lbl)
