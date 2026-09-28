import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POKEDEX_PATH = os.path.join(_ROOT, "data", "pokedex.json")
LEARNSET_PATH = os.path.join(_ROOT, "data", "learnsets.json")
LEARNSETS_MERGED_PATH = os.path.join(_ROOT, "data", "learnsets_merged.json")
POKEMON_CACHE_PATH = os.path.join(_ROOT, "data", "pokemon_cache.pkl")
SELECTED_POKEMON_PATH = os.path.join(_ROOT, "data", "selected_pokemon.json")
CONFIG_FILE_PATH = os.path.join(_ROOT, "data", "config.json")
