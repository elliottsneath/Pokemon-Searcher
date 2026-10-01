"""
Rebuilds data/pokedex.json and data/learnsets.json from Pokémon Showdown, including Pokémon Champions.

Sources:
- Showdown's full pokedex and learnsets (play.pokemonshowdown.com/data).
- Showdown's official Champions mod (smogon/pokemon-showdown, data/mods/champions) for
  Champions-legal species and Champions learnsets.

Every real Pokémon and form is included, including the new Champions/Legends Z-A megas. Fan-made CAP
Pokémon and colour-only variants (Vivillon patterns, Minior colours etc.) are skipped. Learnsets are every move a Pokémon can learn in any
game, with Champions moves merged in. Forms without their own learnset (megas etc.) inherit the
learnset of the form they change from.

Run from the project root:  python data/update_champions_data.py
"""
import json
import os
import re
import urllib.request

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

MOD_URL = "https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/mods/champions"
CHAMPIONS_FORMATS_DATA_URL = f"{MOD_URL}/formats-data.ts"
CHAMPIONS_LEARNSETS_URL = f"{MOD_URL}/learnsets.ts"
POKEDEX_URL = "https://play.pokemonshowdown.com/data/pokedex.json"
LEARNSETS_URL = "https://play.pokemonshowdown.com/data/learnsets.json"

# species whose colour/pattern variants Showdown lists as separate entries
COSMETIC_VARIANT_SPECIES = {"Vivillon", "Minior", "Alcremie", "Deerling", "Sawsbuck", "Burmy", "Shellos"}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Pokemon-Searcher"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def parse_champions_species(formats_data_ts):
    """Returns species ids that are usable in Champions."""
    legal = set()
    for species_id, body in re.findall(r"^\t(\w+): \{(.*?)^\t\},", formats_data_ts, re.M | re.S):
        if "isNonstandard" in body or 'tier: "Illegal"' in body:
            continue
        legal.add(species_id)
    return legal


def parse_champions_learnsets(learnsets_ts):
    """Returns {species_id: set(move_id)} from a Showdown learnsets.ts file."""
    learnsets = {}
    current = None
    for line in learnsets_ts.splitlines():
        species_match = re.match(r"^\t(\w+): \{", line)
        if species_match:
            current = species_match.group(1)
            learnsets[current] = set()
            continue
        move_match = re.match(r"^\t\t\t(\w+): \[", line)
        if move_match and current:
            learnsets[current].add(move_match.group(1))
    return learnsets


def to_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def is_cosmetic_variant(species_id, data, full_pokedex, full_learnsets):
    """True for colour/pattern variants that are identical to their base species (Vivillon-Icy Snow etc.)."""
    base_species = data.get("baseSpecies")
    if base_species not in COSMETIC_VARIANT_SPECIES or species_id in full_learnsets or data.get("forme") == "Gmax":
        return False
    base = full_pokedex[to_id(base_species)]
    return (data.get("types") == base.get("types")
            and data.get("baseStats") == base.get("baseStats")
            and data.get("abilities") == base.get("abilities"))


def main():
    print("Downloading data from Pokemon Showdown...")
    champions_species = parse_champions_species(fetch(CHAMPIONS_FORMATS_DATA_URL))
    champions_learnsets = parse_champions_learnsets(fetch(CHAMPIONS_LEARNSETS_URL))
    full_pokedex = json.loads(fetch(POKEDEX_URL))
    full_learnsets = json.loads(fetch(LEARNSETS_URL))

    pokedex = {}
    for species_id, data in full_pokedex.items():
        # skip MissingNo./Pokestar and fan-made CAP Pokémon
        if data.get("num", 0) <= 0 or data.get("isNonstandard") == "CAP":
            continue
        if is_cosmetic_variant(species_id, data, full_pokedex, full_learnsets):
            continue
        # tiers from the main pokedex are irrelevant here and would mislabel Champions megas as illegal
        data.pop("tier", None)
        data.pop("isNonstandard", None)
        pokedex[species_id] = data

    def moves_for(species_id):
        moves = set(full_learnsets.get(species_id, {}).get("learnset", {}))
        moves |= champions_learnsets.get(species_id, set())
        return moves

    def sv_moves_for(species_id):
        learnset = full_learnsets.get(species_id, {}).get("learnset", {})
        moves = {m for m, codes in learnset.items() if any(c[0] == "9" for c in codes)}
        moves |= champions_learnsets.get(species_id, set())
        return moves

    def build_learnsets(moves_fn):
        result = {}
        for species_id in pokedex:
            moves = moves_fn(species_id)
            current = species_id
            # megas and other battle forms share the learnset of the form they change from,
            # which may itself need to fall back to its base species (e.g. Tatsugiri-Droopy-Mega)
            while not moves and current in full_pokedex:
                data = full_pokedex[current]
                parent = data.get("changesFrom") or data.get("battleOnly") or data.get("baseSpecies")
                if isinstance(parent, list):
                    parent = parent[0]
                if not parent or to_id(parent) == current:
                    break
                current = to_id(parent)
                moves = moves_fn(current)
            if moves:
                result[species_id] = sorted(moves)
        return result

    learnsets = build_learnsets(moves_for)
    sv_learnsets = build_learnsets(sv_moves_for)

    with open(os.path.join(DATA_DIR, "pokedex.json"), "w", encoding="utf-8") as f:
        json.dump(pokedex, f, indent=2)
    with open(os.path.join(DATA_DIR, "learnsets.json"), "w", encoding="utf-8") as f:
        json.dump(learnsets, f, indent=2)
    with open(os.path.join(DATA_DIR, "learnsets_sv.json"), "w", encoding="utf-8") as f:
        json.dump(sv_learnsets, f, indent=2)

    print(f"Saved {len(pokedex)} Pokemon ({len(champions_species & pokedex.keys())} Champions-legal) "
          f"and {len(learnsets)} learnsets ({len(sv_learnsets)} with SV movepools).")


if __name__ == "__main__":
    main()
