"""Loads, saves, and refreshes all Pokémon and config data."""

from __future__ import annotations
import hashlib
import json
import os
import pickle
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import QTimer

from assets.ui.pokemon_list_item import SettingsPokemonListItem
from common.paths import (
    POKEDEX_PATH, LEARNSET_PATH, LEARNSETS_MERGED_PATH,
    POKEMON_CACHE_PATH, SELECTED_POKEMON_PATH, CONFIG_FILE_PATH,
)
from data.pokemon_obj import PokemonData

if TYPE_CHECKING:
    from main import MainWindow


class DataHandler:
    def __init__(self, window: MainWindow):
        self.w = window
        self._merged_learnsets: dict | None = None
        self._settings_build_index = 0
        self.load_pokemon_data(init=True)

    # ── load ───────────────────────────────────────────────────────────────

    def load_pokemon_data(self, init: bool = True) -> None:
        self.w.master_list = []
        self.w.all_names = []
        self.w.all_abilities = set()
        self.w.all_moves = set()

        try:
            if init:
                with open(SELECTED_POKEMON_PATH, 'r') as f:
                    spdata = json.load(f)
                    self.w.selected_pokemon = spdata.get("selected_pokemon", [])
                    self.w.draft_board = spdata.get("draft_board", {})
                    self.w.draft_pools = spdata.get("draft_pools", 0)
                self.w.pokedex = []

            with open(CONFIG_FILE_PATH, 'r') as f:
                favourites = json.load(f)
            if init:
                self.w.pool = favourites.get("pool")
                self.w.hide_drafted = favourites.get("hide_drafted", False)

            self.w.highest_stats = [-float('inf')] * 6
            self.w.lowest_stats = [float('inf')] * 6

            if self._try_load_cache(favourites, init):
                if init:
                    self._populate_settings_list()
                return

            # ── full rebuild ───────────────────────────────────────────────
            with open(POKEDEX_PATH, 'r') as f:
                pokedex = json.load(f)
            with open(LEARNSET_PATH, 'r') as f:
                learnset_data = json.load(f)

            merged = self._ensure_merged_learnsets(pokedex, learnset_data)

            for pokemon, pdata in pokedex.items():
                if init:
                    self.w.pokedex.append(pokemon)
                if pokemon not in self.w.selected_pokemon:
                    continue

                num = pdata.get("num", -1)
                name = pdata.get("name", "")
                types = pdata.get("types", [])
                stats = list(pdata.get("baseStats", {}).values())
                moves = merged.get(pokemon, [])

                base_abilities, hidden_abilities = [], []
                for key, value in pdata.get("abilities", {}).items():
                    (hidden_abilities if key == 'H' else base_abilities).append(value)
                    self.w.all_abilities.add(value)

                for i, stat in enumerate(stats):
                    if stat > self.w.highest_stats[i]: self.w.highest_stats[i] = stat
                    if stat < self.w.lowest_stats[i]: self.w.lowest_stats[i] = stat

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

            self._save_cache()

            if init:
                self._populate_settings_list()

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    # ── pickle cache ───────────────────────────────────────────────────────

    def _selection_fingerprint(self) -> str:
        return hashlib.md5(",".join(sorted(self.w.selected_pokemon)).encode()).hexdigest()

    def _try_load_cache(self, favourites: dict, init: bool) -> bool:
        if not os.path.exists(POKEMON_CACHE_PATH):
            return False
        try:
            source_mtime = max(os.path.getmtime(POKEDEX_PATH), os.path.getmtime(LEARNSET_PATH))
            if os.path.getmtime(POKEMON_CACHE_PATH) <= source_mtime:
                return False
            with open(POKEMON_CACHE_PATH, 'rb') as f:
                cache = pickle.load(f)
            if cache.get("fingerprint") != self._selection_fingerprint():
                return False
            self.w.master_list = cache["master_list"]
            self.w.all_names = cache["all_names"]
            self.w.all_abilities = cache["all_abilities"]
            self.w.all_moves = cache["all_moves"]
            self.w.highest_stats = cache["highest_stats"]
            self.w.lowest_stats = cache["lowest_stats"]
            if init:
                self.w.pokedex = cache["pokedex"]
            for p in self.w.master_list:
                p.favourite = p.name in favourites.get("favourites", [])
                draft_info = self.w.draft_board.get(p.species_id, {})
                p.cost = draft_info.get("cost")
                p.drafted = self.w.pool in draft_info.get("drafted_in", [])
            return True
        except Exception:
            return False

    def _save_cache(self) -> None:
        try:
            with open(POKEMON_CACHE_PATH, 'wb') as f:
                pickle.dump({
                    "fingerprint": self._selection_fingerprint(),
                    "master_list": self.w.master_list,
                    "all_names": self.w.all_names,
                    "all_abilities": self.w.all_abilities,
                    "all_moves": self.w.all_moves,
                    "highest_stats": self.w.highest_stats,
                    "lowest_stats": self.w.lowest_stats,
                    "pokedex": self.w.pokedex,
                }, f)
        except Exception as e:
            print(f"Cache write failed: {e}")

    # ── merged learnsets ───────────────────────────────────────────────────

    def _ensure_merged_learnsets(self, pokedex: dict, learnset_data: dict) -> dict:
        if self._merged_learnsets is not None:
            return self._merged_learnsets
        if os.path.exists(LEARNSETS_MERGED_PATH):
            source_mtime = max(os.path.getmtime(POKEDEX_PATH), os.path.getmtime(LEARNSET_PATH))
            if os.path.getmtime(LEARNSETS_MERGED_PATH) > source_mtime:
                with open(LEARNSETS_MERGED_PATH, 'r') as f:
                    self._merged_learnsets = json.load(f)
                return self._merged_learnsets
        self._merged_learnsets = self._build_merged_learnsets(pokedex, learnset_data)
        with open(LEARNSETS_MERGED_PATH, 'w') as f:
            json.dump(self._merged_learnsets, f)
        return self._merged_learnsets

    def _build_merged_learnsets(self, pokedex: dict, learnset_data: dict) -> dict:
        memo: dict[str, set] = {}

        def get_moves(key, visiting=None):
            if key in memo:
                return memo[key]
            if visiting is None:
                visiting = set()
            if key in visiting or key not in pokedex:
                return set()
            visiting.add(key)
            moves = set(learnset_data.get(key, []))
            prevo_name = pokedex[key].get("prevo")
            if prevo_name:
                for prevo_key, prevo_data in pokedex.items():
                    if prevo_data.get("name") == prevo_name:
                        moves.update(get_moves(prevo_key, visiting))
                        break
            memo[key] = moves
            return moves

        return {pk: sorted(get_moves(pk)) for pk in pokedex}

    # ── settings list (batched) ────────────────────────────────────────────

    def _populate_settings_list(self) -> None:
        self._settings_build_index = 0
        self._settings_batch()

    def _settings_batch(self) -> None:
        batch_size = 50
        subset = self.w.pokedex[self._settings_build_index:self._settings_build_index + batch_size]
        for pokemon in subset:
            widget = SettingsPokemonListItem(pokemon)
            if pokemon in self.w.selected_pokemon:
                widget.checkbox.setChecked(True)
            item = QListWidgetItem(self.w.settingsPokemonListWidget)
            item.setSizeHint(widget.sizeHint())
            self.w.settingsPokemonListWidget.addItem(item)
            self.w.settingsPokemonListWidget.setItemWidget(item, widget)
        self._settings_build_index += batch_size
        if self._settings_build_index < len(self.w.pokedex):
            QTimer.singleShot(0, self._settings_batch)

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
        for pokemon in self.w.master_list:
            draft_info = self.w.draft_board.get(pokemon.species_id, {})
            pokemon.cost = draft_info.get("cost")
            pokemon.drafted = self.w.pool in draft_info.get("drafted_in", [])
