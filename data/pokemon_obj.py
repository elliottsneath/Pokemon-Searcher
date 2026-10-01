from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from common.draft_format import DraftFormat


@dataclass
class PokemonData:
    num: int
    name: str
    types: List[str]
    base_abilities: List[str]
    hidden_abilities: List[str]
    stats: List[int]
    moves: List[str]
    favourite: bool = False
    species_id: str = ""
    cost: Optional[int] = None
    drafted: bool = False
    sv_moves: List[str] = field(default_factory=list)

    def moves_for(self, fmt: DraftFormat) -> List[str]:
        from common.draft_format import DraftFormat as DF
        if fmt in (DF.SV, DF.CHAMPIONS):
            return getattr(self, "sv_moves", None) or self.moves
        return self.moves