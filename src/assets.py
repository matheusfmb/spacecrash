"""
Carregador central de assets.
"""

from pathlib import Path

import pygame

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"


class AssetManager:
    def __init__(self):
        self._images = {}
        self._sounds = {}
        self._fonts = {}

    def image(self, relative_path, convert_alpha=True):
        """Carrega (ou reaproveita do cache) uma imagem de assets/<relative_path>."""
        key = (relative_path, convert_alpha)
        if key not in self._images:
            surface = pygame.image.load(str(ASSETS_DIR / relative_path))
            self._images[key] = (
                surface.convert_alpha() if convert_alpha else surface.convert()
            )
        return self._images[key]

    def sound(self, relative_path):
        if relative_path not in self._sounds:
            self._sounds[relative_path] = pygame.mixer.Sound(
                str(ASSETS_DIR / relative_path)
            )
        return self._sounds[relative_path]

    def font(self, relative_path, size):
        key = (relative_path, size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(str(ASSETS_DIR / relative_path), size)
        return self._fonts[key]

    def load_music(self, relative_path):
        pygame.mixer.music.load(str(ASSETS_DIR / relative_path))
