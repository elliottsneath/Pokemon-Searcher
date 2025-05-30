from dataclasses import dataclass
from typing import List

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