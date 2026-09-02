"""A moeda que dá pontos ao ser coletada."""

import random

import pygame

import settings
from src.animation import Animation
from src.effects import build_coin_spin_frames


class Coin(pygame.sprite.Sprite):
    def __init__(self, assets):
        super().__init__()
        self._base_image = assets.image(settings.COIN_IMAGE)
        self.spin_anim = Animation(build_coin_spin_frames(self._base_image), frame_duration=0.09, loop=True)
        self.image = self.spin_anim.current_frame()
        self.pos = pygame.Vector2(0, 0)
        self.rect = self.image.get_rect()
        self.respawn(at_top=True)

    def respawn(self, at_top=False):
        self.pos.x = random.randrange(0, settings.SCREEN_W - self._base_image.get_width())
        self.pos.y = -40 if at_top else -150
        self._sync_rect()

    def _sync_rect(self):
        self.image = self.spin_anim.current_frame()
        self.rect = self.image.get_rect(
            center=(
                round(self.pos.x + self._base_image.get_width() / 2),
                round(self.pos.y + self._base_image.get_height() / 2),
            )
        )

    def update(self, dt):
        self.pos.y += settings.COIN_SPEED * dt
        self.spin_anim.update(dt)
        self._sync_rect()
        if self.pos.y > settings.SCREEN_H:
            self.respawn()
