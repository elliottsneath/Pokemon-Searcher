import json
import os
import re
import urllib.request

from PySide6.QtGui import QPixmap

_SPRITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sprites")
_POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/{}"


def _to_slug(name: str) -> str:
    name = name.lower()
    name = re.sub(r"\.\s", "-", name)   # "Mr. Mime" → "mr-mime"
    name = re.sub(r"[.:''‘’]", "", name)  # remove punctuation
    name = name.replace(" ", "-")
    return re.sub(r"-+", "-", name).strip("-")


def get_sprite(species_id: str, name: str) -> QPixmap | None:
    os.makedirs(_SPRITE_DIR, exist_ok=True)
    path = os.path.join(_SPRITE_DIR, f"{species_id}.png")
    if not os.path.exists(path):
        try:
            slug = _to_slug(name)
            req = urllib.request.Request(_POKEAPI_URL.format(slug), headers={"User-Agent": "pokemon-searcher"})
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read())
            sprite_url = data["sprites"]["other"]["official-artwork"]["front_default"]
            if not sprite_url:
                return None
            urllib.request.urlretrieve(sprite_url, path)
        except Exception:
            return None
    pix = QPixmap(path)
    return pix if not pix.isNull() else None
