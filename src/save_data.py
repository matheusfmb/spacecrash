"""
Salva e carrega as preferências de áudio
"""

import json
from pathlib import Path

import settings

SAVE_PATH = Path(__file__).resolve().parent.parent / settings.SAVE_FILE


def load():
    """Lê o save; se não existir ou estiver corrompido, volta os padrões."""
    defaults = {
        "music_volume": settings.MUSIC_VOLUME,
        "sfx_volume": settings.DEFAULT_SFX_VOLUME,
    }
    if not SAVE_PATH.exists():
        return defaults

    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        return {
            "music_volume": float(data.get("music_volume", defaults["music_volume"])),
            "sfx_volume": float(data.get("sfx_volume", defaults["sfx_volume"])),
        }
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return defaults


def save(music_volume, sfx_volume):
    data = {"music_volume": music_volume, "sfx_volume": sfx_volume}
    try:
        SAVE_PATH.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass  # sem permissão de escrita, por exemplo — não trava o jogo por isso
