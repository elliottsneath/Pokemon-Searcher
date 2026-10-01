from __future__ import annotations

from typing import Callable

from PySide6.QtWidgets import QLayout

from common.custom_widgets import type_count_widget
from common.draft_format import DraftFormat
from common.helpers import clear_layout
from common.type_chart import effectiveness
from data.pokemon_obj import PokemonData


class DraftAnalysis:
    HP  = 0
    ATK = 1
    DEF = 2
    SPA = 3
    SPD = 4
    SPE = 5

    ARCHETYPES: dict[str, Callable[[PokemonData, DraftFormat], bool]] = {
        "Bulky Water":      lambda p, _: "Water" in p.types and p.stats[DraftAnalysis.DEF] + p.stats[DraftAnalysis.SPD] >= 170,
        "Grounded Poison":  lambda p, _: "Poison" in p.types and "Flying" not in p.types and "Levitate" not in DraftAnalysis.all_abilities(p),
        "Physical Breaker": lambda p, _: p.stats[DraftAnalysis.ATK] >= 125,
        "Special Breaker":  lambda p, _: p.stats[DraftAnalysis.SPA] >= 125,
        "Pivot":            lambda p, f: any(m in p.moves_for(f) for m in ("uturn", "voltswitch", "flipturn", "partingshot", "teleport")),
        "Stealth Rock":     lambda p, f: "stealthrock" in p.moves_for(f),
        "Spikes":           lambda p, f: "spikes" in p.moves_for(f),
        "Hazard Removal":   lambda p, f: any(m in p.moves_for(f) for m in ("rapidspin", "defog", "mortalspin", "tidyup", "courtchange")),
        "Knock Off":        lambda p, f: "knockoff" in p.moves_for(f),
        "Trick Room":       lambda p, f: "trickroom" in p.moves_for(f),
        "Cleric":           lambda p, f: any(m in p.moves_for(f) for m in ("healbell", "aromatherapy", "lunardance")),
        "Physical Wall":    lambda p, _: p.stats[DraftAnalysis.DEF] >= 100 and p.stats[DraftAnalysis.HP] >= 80,
        "Special Wall":     lambda p, _: p.stats[DraftAnalysis.SPD] >= 100 and p.stats[DraftAnalysis.HP] >= 80,
        "Speed Control":    lambda p, f: p.stats[DraftAnalysis.SPE] >= 110 or any(m in p.moves_for(f) for m in ("tailwind", "trickroom", "stickywebs", "thunderwave")),
        "Contact Punish":   lambda p, _: any(a in DraftAnalysis.all_abilities(p) for a in ("Rough Skin", "Iron Barbs", "Static", "Flame Body")) and p.stats[DraftAnalysis.DEF] >= 80,
        "Spinblocker":      lambda p, _: "Ghost" in p.types,
        "Fast Mon":         lambda p, _: p.stats[DraftAnalysis.SPE] >= 115,
        "Sleeper":          lambda p, f: any(m in p.moves_for(f) for m in ("spore",)),
    }

    def __init__(self, weaknesses_layout: QLayout, resistances_layout: QLayout, immunities_layout: QLayout):
        self.weaknesses_layout = weaknesses_layout
        self.resistances_layout = resistances_layout
        self.immunities_layout = immunities_layout
        self.type_scores: dict[str, int] = {}
        self.all_types: list[str] = []
        self.missing_roles: set[str] = set(self.ARCHETYPES.keys())
        self.fmt: DraftFormat = DraftFormat.CHAMPIONS_NATDEX

    @staticmethod
    def all_abilities(p: PokemonData) -> list[str]:
        return p.base_abilities + p.hidden_abilities

    @staticmethod
    def score(eff: float) -> int:
        if eff >= 4:    return 2
        if eff > 1:     return 1
        if eff == 0:    return -2
        if eff <= 0.25: return -2
        if eff < 1:     return -1
        return 0

    @staticmethod
    def safe_check(check: Callable[[PokemonData, DraftFormat], bool], p: PokemonData, fmt: DraftFormat) -> bool:
        try:
            return check(p, fmt)
        except Exception:
            return False

    @staticmethod
    def find_missing_roles(drafted_pokemon: list[PokemonData | None], fmt: DraftFormat) -> set[str]:
        covered: set[str] = set()
        for p in drafted_pokemon:
            if p is None:
                continue
            for role, check in DraftAnalysis.ARCHETYPES.items():
                if DraftAnalysis.safe_check(check, p, fmt):
                    covered.add(role)
        return set(DraftAnalysis.ARCHETYPES.keys()) - covered

    @staticmethod
    def weakness_improvement(pokemon: PokemonData, type_scores: dict[str, int], all_types: list[str]) -> float:
        delta = 0.0
        for atk_type in all_types:
            old = type_scores.get(atk_type, 0)
            new = old + DraftAnalysis.score(effectiveness(atk_type, pokemon.types))
            delta += max(0, old) - max(0, new)
        return delta

    def update(self, drafted_pokemon: list[PokemonData | None], all_types: list[str], fmt: DraftFormat = DraftFormat.CHAMPIONS_NATDEX) -> None:
        active = [p for p in drafted_pokemon if p is not None]

        type_scores: dict[str, int] = {}
        immunity_counts: dict[str, int] = {}

        for pokemon in active:
            for atk in all_types:
                eff = effectiveness(atk, pokemon.types)
                if eff == 0:
                    immunity_counts[atk] = immunity_counts.get(atk, 0) + 1
                s = self.score(eff)
                if s:
                    type_scores[atk] = type_scores.get(atk, 0) + s

        self.type_scores = type_scores
        self.all_types = all_types
        self.fmt = fmt
        self.missing_roles = self.find_missing_roles(drafted_pokemon, fmt)

        top_weak   = sorted(((t, s) for t, s in type_scores.items() if s > 0), key=lambda x: -x[1])[:3]
        top_resist = sorted(((t, s) for t, s in type_scores.items() if s < 0), key=lambda x:  x[1])[:3]
        immunities = sorted(immunity_counts.items(), key=lambda x: -x[1])[:3]

        self.set_icons(self.weaknesses_layout, [(t, f"+{s}") for t, s in top_weak])
        self.set_icons(self.resistances_layout, [(t, str(s)) for t, s in top_resist])
        self.set_icons(self.immunities_layout,  [(t, f"x{c}") for t, c in immunities])

    def update_recommendations(
        self,
        drafted_pokemon: list[PokemonData | None],
        available_pokemon: list[PokemonData],
        per_pick_budget: float,
    ) -> list[tuple[PokemonData, list[str]]]:
        def matched_roles(p: PokemonData) -> list[str]:
            return [r for r, check in self.ARCHETYPES.items() if r in self.missing_roles and self.safe_check(check, p, self.fmt)]

        pool = [
            p for p in available_pokemon
            if p not in drafted_pokemon
            and (per_pick_budget <= 0 or p.cost is None or p.cost <= per_pick_budget)
        ]

        candidates = [(p, matched_roles(p)) for p in pool]
        candidates_with_roles = [(p, roles) for p, roles in candidates if roles]

        if candidates_with_roles:
            candidates_with_roles.sort(
                key=lambda x: (len(x[1]), self.weakness_improvement(x[0], self.type_scores, self.all_types)),
                reverse=True,
            )
            return candidates_with_roles[:3]

        pool.sort(key=lambda p: (p.cost or 0, self.weakness_improvement(p, self.type_scores, self.all_types)), reverse=True)
        return [(p, []) for p in pool[:3]]

    @staticmethod
    def set_icons(layout: QLayout, entries: list[tuple[str, str]]) -> None:
        clear_layout(layout)
        for t, label in entries:
            layout.addWidget(type_count_widget(t, label))
