"""Pure functions for normalising Pokémon names and parsing the DDL draft board Excel sheet."""

import re
import pandas as pd


UNWANTED_STRINGS = {
    "normal", "fire", "water", "electric", "grass", "ice", "fighting",
    "poison", "ground", "flying", "psychic", "bug", "rock", "ghost",
    "dragon", "dark", "steel", "fairy", "formatting", "drafted",
    "terarestricted", "complex", "fullyevolved", "0", "nfes", "nan", "↑", "20.0",
    "19.0", "18.0", "17.0", "16.0", "15.0", "14.0", "13.0", "12.0", "11.0", "10.0",
    "9.0", "8.0", "7.0", "6.0", "5.0", "4.0", "3.0", "2.0", "1.0", "1pointnfes",
    "20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "10",
    "9", "8", "7", "6", "5", "4", "3", "2", "1", "<3", "28", "banned", "tb", "",
    "20 points", "19 points", "p1", "p2", "p3", "p4", "p5", "18 points", "17 points", "16 points",
    "15 points", "14 points", "13 points", "12 points", "11 points", "10 points", "9 points",
    "8 points", "7 points", "6 points", "5 points", "4 points", "3 points", "2 points",
    "1 point", "x", "✓",
}

_REGION_MAP = {"Alolan": "alola", "Galarian": "galar", "Hisuian": "hisui", "Paldean": "paldea"}


def _unique_cases(p: str) -> str:
    lp = p.lower()
    if "lycanroc" in lp:
        if "midday" in lp:   return "Lycanroc"
        if "dusk" in lp:     return "LycanrocDusk"
        if "midnight" in lp: return "LycanrocMidnight"
        return p.replace("rock", "roc")
    if lp == "mime jr.":          return "mimejr"
    if "bloodmoon" in lp or ("ursaluna" in lp and lp.endswith("-b")):
        return "ursalunabloodmoon"
    if "defence" in lp:           return p.replace("Defence", "defense")
    if " rotom" in lp:            return f"rotom{p.split(' ')[0]}"
    if "ogerpon" in lp:
        if "cornerstone" in lp or lp.endswith("-c"): return "ogerponcornerstone"
        if "hearthflame" in lp or lp.endswith("-h"):  return "ogerponhearthflame"
        if "wellspring" in lp or lp.endswith("-w"):   return "ogerponwellspring"
        return "ogerpon"
    if " kyurem" in lp:           return f"kyurem{p.split(' ')[0]}"
    if "incarnate" in lp:         return p.split(" ")[0]
    if "therian" in lp:           return f"{p.replace('-', ' ').split()[0]}therian"
    if lp == "cheems-pao":        return "chienpao"
    if lp == "mega charizard x":  return "charizardmegax"
    if lp == "mega charizard y":  return "charizardmegay"
    if lp == "mega mewtwo x":     return "mewtwomegax"
    if lp == "mega mewtwo y":     return "mewtwomegay"
    if lp == "mega raichu x":     return "raichumegax"
    if lp == "mega raichu y":     return "raichumegay"
    if lp == "mega tatsugiri":    return "tatsugiricurlymega"
    if "dawn wings" in lp:        return "necrozmadawnwings"
    if "dusk mane" in lp:         return "necrozmaduskmane"
    if "single strike" in lp:     return "urshifu"
    if "rapid strike" in lp:      return "urshifurapidstrike"
    if "ice rider" in lp:         return "calyrexice"
    if "shadow rider" in lp:      return "calyrexshadow"
    if "eternal" in lp or ("floette" in lp and lp.endswith("-e")):
        return "floetteeternal"
    if "tauros" in lp:
        if "aqua" in lp:    return "taurospaldeaaqua"
        if "blaze" in lp:   return "taurospaldeablaze"
        if "combat" in lp:  return "taurospaldeacombat"
        if "paldean" in lp: return f"taurospaldea{p.split(' ')[2]}"
    if lp in ("meowstic-mega", "mega meowstic"): return "meowsticmmega"
    if "primal" in lp:
        parts = p.split()
        if len(parts) >= 2: return f"{parts[1]}primal"
    if "zamazenta" in lp:  return "zamazentacrowned" if "crowned" in lp else "zamazenta"
    if "zacian" in lp:     return "zaciancrowned" if "crowned" in lp else "zacian"
    if "shaymin" in lp:    return "shayminsky" if "sky" in lp else "shaymin"
    if "zygarde" in lp:
        if "complete" in lp:  return "zygardecomplete"
        if "10" in lp:        return "zygarde10"
        return "zygarde"
    if "oinkologne" in lp: return "oinkolognef" if "female" in lp else "oinkologne"
    return p


def normalise_pokemon(pokemon) -> str | None:
    if not isinstance(pokemon, str):
        return None
    p = re.sub(r'[\n\r]+', ' ', pokemon.strip())
    p = re.sub(r' +', ' ', p).strip()
    p = _unique_cases(p)
    if "Mega " in p:
        p = f"{p[5:]}mega"
    p = (p.replace("'", "").replace(". ", "").replace("-", "")
          .replace("é", "e").replace("♀", "f").replace("♂", "m")
          .replace("%", "").replace(": ", ""))
    for region, suffix in _REGION_MAP.items():
        if region in p:
            parts = p.split(" ")
            return f"{parts[1]}{suffix}".lower() if len(parts) > 1 else None
    p = re.sub(r'\s+[Ff]orme?$', '', p)
    return p.replace(" ", "").lower()


def parse_draft_board(xls, target_sheet: str, pokedex: list) -> tuple[dict, int]:
    """Returns (draft_board dict, draft_pools count) from a draft board Excel sheet.

    draft_board: {species_id: {"cost": int, "drafted_in": [pool_numbers]}}
    """
    grid = pd.read_excel(xls, sheet_name=target_sheet, header=None, engine='openpyxl')
    draft_board: dict = {}
    draft_pools: int = 0

    for header_row in range(grid.shape[0]):
        for col in range(grid.shape[1] - 1):
            cell = str(grid.iat[header_row, col]).strip()

            # DDL format: "N Points" / "N Point" header with pool columns
            ddl_match = re.fullmatch(r"(\d+) Points?", cell)
            if ddl_match:
                cost = int(ddl_match.group(1))

                pool_cols: list[tuple[int, int]] = []
                pc = col + 2
                while pc < grid.shape[1]:
                    pm = re.fullmatch(r"P(\d+)", str(grid.iat[header_row, pc]).strip())
                    if not pm:
                        break
                    pool_cols.append((int(pm.group(1)), pc))
                    pc += 1
                draft_pools = max(draft_pools, len(pool_cols))

                for row in range(header_row + 1, grid.shape[0]):
                    key = normalise_pokemon(grid.iat[row, col + 1])
                    if key not in pokedex:
                        continue
                    draft_board[key] = {
                        "cost": cost,
                        "drafted_in": [p for p, c in pool_cols
                                       if str(grid.iat[row, c]).strip().upper() == "X"],
                    }
                continue

            # ODL format: plain integer cost preceded by "a" separator column
            if col >= 1 and str(grid.iat[header_row, col - 1]).strip().lower() == "a":
                try:
                    cost = int(float(cell))
                except (ValueError, TypeError):
                    continue
                if not 1 <= cost <= 30:
                    continue

                x_col = col + 1
                for row in range(header_row + 1, grid.shape[0]):
                    key = normalise_pokemon(grid.iat[row, col])
                    if key not in pokedex:
                        continue
                    drafted = x_col < grid.shape[1] and str(grid.iat[row, x_col]).strip().upper() == "X"
                    draft_board[key] = {"cost": cost, "drafted_in": [1] if drafted else []}

    return draft_board, draft_pools
