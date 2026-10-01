import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POKEDEX_PATH = os.path.join(_ROOT, "data", "pokedex.json")
LEARNSET_PATH = os.path.join(_ROOT, "data", "learnsets.json")
LEARNSETS_SV_PATH = os.path.join(_ROOT, "data", "learnsets_sv.json")
LEARNSETS_MERGED_PATH = os.path.join(_ROOT, "data", "learnsets_merged.json")
LEARNSETS_SV_MERGED_PATH = os.path.join(_ROOT, "data", "learnsets_sv_merged.json")
POKEMON_CACHE_PATH = os.path.join(_ROOT, "data", "pokemon_cache.pkl")
SELECTED_POKEMON_PATH = os.path.join(_ROOT, "data", "selected_pokemon.json")
CONFIG_FILE_PATH = os.path.join(_ROOT, "data", "config.json")
DRAFT_STATE_PATH = os.path.join(_ROOT, "data", "draft_state.json")
