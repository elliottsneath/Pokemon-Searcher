from dataclasses import dataclass
from typing import List, Optional

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