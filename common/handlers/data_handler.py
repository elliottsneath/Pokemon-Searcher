"""Loads, saves, and refreshes all Pokémon and config data."""

from __future__ import annotations
import json
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QListWidgetItem

from assets.ui.pokemon_list_item import SettingsPokemonListItem
from common.paths import POKEDEX_PATH, LEARNSET_PATH, SELECTED_POKEMON_PATH, CONFIG_FILE_PATH
from data.pokemon_obj import PokemonData

if TYPE_CHECKING:
    from main import MainWindow


class DataHandler:
    def __init__(self, window: MainWindow):
        self.w = window
        self.load_pokemon_data(init=True)

    # ── load ───────────────────────────────────────────────────────────────

    def load_pokemon_data(self, init: bool = True) -> None:
        self.w.master_list = []
        self.w.all_names = []
        self.w.all_abilities = set()
        self.w.all_moves = set()

        try:
            with open(POKEDEX_PATH, 'r') as f:
                pokedex = json.load(f)
            if init:
                with open(SELECTED_POKEMON_PATH, 'r') as f:
                    spdata = json.load(f)
                    self.w.selected_pokemon = spdata.get("selected_pokemon", [])
                    self.w.draft_board = spdata.get("draft_board", {})
                    self.w.draft_pools = spdata.get("draft_pools", 0)
            with open(LEARNSET_PATH, 'r') as f:
                learnset_data = json.load(f)
            with open(CONFIG_FILE_PATH, 'r') as f:
                favourites = json.load(f)
            if init:
                self.w.pool = favourites.get("pool")
                self.w.hide_drafted = favourites.get("hide_drafted", False)

            self.w.highest_stats = [-float('inf')] * 6
            self.w.lowest_stats = [float('inf')] * 6
            if init:
                self.w.pokedex = []

            def get_all_prevo_moves(pokemon_key, visited=None):
                if visited is None:
                    visited = set()
                if pokemon_key in visited:
                    return set()
                visited.add(pokemon_key)
                moves = set(learnset_data.get(pokemon_key, []))
                prevo_name = pokedex[pokemon_key].get("prevo")
                if prevo_name:
                    for prevo_key, prevo_data in pokedex.items():
                        if prevo_data.get("name") == prevo_name:
                            moves.update(get_all_prevo_moves(prevo_key, visited))
                            break
                return moves

            for pokemon, pdata in pokedex.items():
                if init:
                    self.w.pokedex.append(pokemon)
                    widget = SettingsPokemonListItem(pokemon)
                    if pokemon in self.w.selected_pokemon:
                        widget.checkbox.setChecked(True)
                    item = QListWidgetItem(self.w.settingsPokemonListWidget)
                    item.setSizeHint(widget.sizeHint())
                    self.w.settingsPokemonListWidget.addItem(item)
                    self.w.settingsPokemonListWidget.setItemWidget(item, widget)

                if pokemon not in self.w.selected_pokemon:
                    continue

                num   = pdata.get("num", -1)
                name  = pdata.get("name", "")
                types = pdata.get("types", [])
                stats = list(pdata.get("baseStats", {}).values())
                moves = sorted(get_all_prevo_moves(pokemon))

                base_abilities, hidden_abilities = [], []
                for key, value in pdata.get("abilities", {}).items():
                    (hidden_abilities if key == 'H' else base_abilities).append(value)
                    self.w.all_abilities.add(value)

                for i, stat in enumerate(stats):
                    if stat > self.w.highest_stats[i]: self.w.highest_stats[i] = stat
                    if stat < self.w.lowest_stats[i]:  self.w.lowest_stats[i] = stat

                draft_info = self.w.draft_board.get(pokemon, {})
                self.w.master_list.append(PokemonData(
                    num=num, name=name, types=types,
                    base_abilities=base_abilities, hidden_abilities=hidden_abilities,
                    stats=stats, moves=moves,
                    favourite=name in favourites.get("favourites", []),
                    species_id=pokemon,
                    cost=draft_info.get("cost"),
                    drafted=self.w.pool in draft_info.get("drafted_in", []),
                ))
                self.w.all_names.append(name)

            for moves_list in learnset_data.values():
                self.w.all_moves.update(moves_list)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    # ── save ───────────────────────────────────────────────────────────────

    def selected_pokemon_json(self) -> dict:
        return {
            "selected_pokemon": self.w.selected_pokemon,
            "draft_pools": self.w.draft_pools,
            "draft_board": self.w.draft_board,
        }

    def save_selected_pokemon(self) -> None:
        with open(SELECTED_POKEMON_PATH, "w") as f:
            json.dump(self.selected_pokemon_json(), f, indent=4)

    def save_config(self) -> None:
        loaded_names = {p.name for p in self.w.master_list}
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                saved_favourites = json.load(f).get("favourites", [])
        except (FileNotFoundError, json.JSONDecodeError):
            saved_favourites = []
        favourite_names = (
            [name for name in saved_favourites if name not in loaded_names] +
            [p.name for p in self.w.master_list if p.favourite]
        )
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump({
                "favourites": favourite_names,
                "pool": self.w.pool,
                "hide_drafted": self.w.hide_drafted,
            }, f, indent=4)

    # ── refresh ────────────────────────────────────────────────────────────

    def refresh_draft_status(self) -> None:
        """Updates cost and drafted state on master_list from draft_board + selected pool."""
        for pokemon in self.w.master_list:
            draft_info = self.w.draft_board.get(pokemon.species_id, {})
            pokemon.cost = draft_info.get("cost")
            pokemon.drafted = self.w.pool in draft_info.get("drafted_in", [])
