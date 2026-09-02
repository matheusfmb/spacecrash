"""
Controle central de volume do jogo.
"""

import pygame

import settings
from src import save_data


class AudioSettings:
    def __init__(self, music_volume, sfx_volume):
        self.music_volume = _clamp(music_volume)
        self.sfx_volume = _clamp(sfx_volume)
        self._sfx_sources = []  # [(pygame.mixer.Sound, volume_base), ...]

    @classmethod
    def load(cls):
        data = save_data.load()
        return cls(data["music_volume"], data["sfx_volume"])

    def save(self):
        save_data.save(self.music_volume, self.sfx_volume)

    def register_sfx(self, sound, base_volume):
        """Registra um som pra ele passar a ser afetado pelo volume de SFX."""
        self._sfx_sources.append((sound, base_volume))
        sound.set_volume(base_volume * self.sfx_volume)

    def apply_music_volume(self):
        pygame.mixer.music.set_volume(self.music_volume)

    def set_music_volume(self, value):
        self.music_volume = _clamp(value)
        self.apply_music_volume()

    def set_sfx_volume(self, value):
        self.sfx_volume = _clamp(value)
        for sound, base_volume in self._sfx_sources:
            sound.set_volume(base_volume * self.sfx_volume)

    def adjust_music_volume(self, delta):
        self.set_music_volume(self.music_volume + delta)

    def adjust_sfx_volume(self, delta):
        self.set_sfx_volume(self.sfx_volume + delta)


def _clamp(value):
    return max(0.0, min(1.0, value))
