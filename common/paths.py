import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POKEDEX_PATH = os.path.join(_ROOT, "data", "pokedex.json")
LEARNSET_PATH = os.path.join(_ROOT, "data", "learnsets.json")
SELECTED_POKEMON_PATH = os.path.join(_ROOT, "data", "selected_pokemon.json")
CONFIG_FILE_PATH = os.path.join(_ROOT, "data", "config.json")
