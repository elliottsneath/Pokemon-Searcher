from __future__ import annotations
import json
import os
from datetime import datetime
from typing import TYPE_CHECKING

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel

from common.draft_analysis import DraftAnalysis
from common.paths import DRAFT_STATE_PATH
from common.sprite_loader import get_sprite
from common.widget_groups import DraftHandlerWidgets, PickSlot, RecSlot
from data.pokemon_obj import PokemonData

if TYPE_CHECKING:
    from main import MainWindow


class DraftHandler:
    def __init__(self, window: MainWindow, widgets: DraftHandlerWidgets):
        self.w = window
        self.wg = widgets
        self.drafted_pokemon: list[PokemonData | None] = [None] * 12
        self._rec_pokemon: list[PokemonData | None] = [None] * 3
        self._last_import: datetime | None = None
        self._analysis = DraftAnalysis(
            self.wg.weaknesses_layout,
            self.wg.resistances_layout,
            self.wg.immunities_layout,
        )
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
        self.wg.number_of_pokemon_line_edit.textChanged.connect(self.analyse_team_matchups)
        self.wg.number_of_pokemon_line_edit.textChanged.connect(self.update_picks_label)
        self.wg.number_of_pokemon_line_edit.textChanged.connect(self._save_draft_state)
        for i, slot in enumerate(self.wg.rec_slots):
            slot.add_button.clicked.connect(self._make_rec_add_handler(i))
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
        self.analyse_team_matchups()

    def remove_from_draft(self, pokemon: PokemonData) -> None:
        try:
            idx = self.drafted_pokemon.index(pokemon)
        except ValueError:
            return
        self.drafted_pokemon[idx] = None
        self._clear_slot(self.wg.picks[idx], idx)
        self.update_budget()
        self.update_picks_label()
        self.analyse_team_matchups()

    def update_budget(self) -> None:
        text = self.wg.budget_line_edit.text()
        budget = int(text) if text else 0
        spent = sum(p.cost for p in self.drafted_pokemon if p is not None and p.cost is not None)
        self.wg.pts_label.setText(f"{budget - spent} Pts Remaining")
        self._save_draft_state()

    # ── team matchup analysis ─────────────────────────────────────────────────

    def analyse_team_matchups(self) -> None:
        self._analysis.update(self.drafted_pokemon, self.w.all_types)
        budget_text = self.wg.budget_line_edit.text()
        budget = int(budget_text) if budget_text else 0
        spent = sum(p.cost for p in self.drafted_pokemon if p is not None and p.cost is not None)
        budget_remaining = budget - spent

        if budget > 0 and budget_remaining <= 0:
            self._populate_rec_slots([])
            return

        no_of_pokemon_text = self.wg.number_of_pokemon_line_edit.text()
        no_of_pokemon = int(no_of_pokemon_text) if no_of_pokemon_text else 0
        drafted_count = sum(1 for p in self.drafted_pokemon if p is not None)
        remaining_picks = max(no_of_pokemon - drafted_count, 1)
        per_pick_budget = budget_remaining - (remaining_picks - 1) if budget_remaining > 0 else 0

        results = self._analysis.update_recommendations(
            self.drafted_pokemon,
            self.w.master_list,
            per_pick_budget,
        )
        self._populate_rec_slots(results)

    def record_import(self) -> None:
        self._last_import = datetime.now()
        self._update_import_label()
        self._save_draft_state()

    def _update_import_label(self) -> None:
        if self._last_import is None:
            self.wg.refresh_label.setText("Not yet imported")
            return
        delta = datetime.now() - self._last_import
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            text = "Imported just now"
        elif total_seconds < 3600:
            m = total_seconds // 60
            text = f"Imported {m}m ago"
        elif delta.days == 0:
            h = total_seconds // 3600
            text = f"Imported {h}h ago"
        else:
            text = f"Imported {delta.days}d ago"
        self.wg.refresh_label.setText(text)

    def _save_draft_state(self) -> None:
        try:
            with open(DRAFT_STATE_PATH, "w") as f:
                json.dump({
                    "drafted": [p.species_id if p is not None else None for p in self.drafted_pokemon],
                    "budget": self.wg.budget_line_edit.text(),
                    "no_of_pokemon": self.wg.number_of_pokemon_line_edit.text(),
                    "last_import": self._last_import.isoformat() if self._last_import else None,
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
            if no_of_pokemon := data.get("no_of_pokemon"):
                self.wg.number_of_pokemon_line_edit.setText(str(no_of_pokemon))
            if ts := data.get("last_import"):
                self._last_import = datetime.fromisoformat(ts)
            self._update_import_label()
            self.update_picks_label()
            self.analyse_team_matchups()
        except Exception as e:
            print(f"Draft state load failed: {e}")

    def update_picks_label(self) -> None:
        count = sum(1 for p in self.drafted_pokemon if p is not None)
        text = self.wg.number_of_pokemon_line_edit.text()
        total = int(text) if text else 12
        self.wg.picks_label.setText(f"{count}/{total} Picks")

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

    def _make_rec_add_handler(self, idx: int):
        def handler():
            p = self._rec_pokemon[idx]
            if p is not None:
                self.add_to_draft(p)
        return handler

    def _populate_rec_slots(self, results: list[tuple[PokemonData, list[str]]]) -> None:
        for i, slot in enumerate(self.wg.rec_slots):
            if i < len(results):
                p, roles = results[i]
                self._rec_pokemon[i] = p
                self._fill_rec_slot(slot, p, roles)
            else:
                self._rec_pokemon[i] = None
                self._clear_rec_slot(slot)

    def _fill_rec_slot(self, slot: RecSlot, p: PokemonData, roles: list[str]) -> None:
        sprite = get_sprite(p.species_id, p.name)
        if sprite:
            slot.sprite.setPixmap(sprite.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            slot.sprite.clear()
        slot.name.setText(p.name)
        slot.pts.setText(f"{p.cost} pts" if p.cost is not None else "")
        slot.reason.setText(", ".join(roles[:3]) if roles else "Coverage")
        self._set_rec_type_icons(slot, p.types)

    def _clear_rec_slot(self, slot: RecSlot) -> None:
        slot.sprite.clear()
        slot.name.setText("")
        slot.pts.setText("")
        slot.reason.setText("")
        self._set_rec_type_icons(slot, [])

    def _set_rec_type_icons(self, slot: RecSlot, types: list[str]) -> None:
        layout = slot.type_layout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for t in types:
            lbl = QLabel()
            pix = QPixmap(os.path.join("assets", "icons", f"{t.lower()}.svg"))
            if not pix.isNull():
                lbl.setPixmap(pix.scaled(18, 18))
            else:
                lbl.setText(t)
            layout.addWidget(lbl)

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
