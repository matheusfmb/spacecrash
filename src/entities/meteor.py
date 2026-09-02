"""
Um meteoro que desce a tela.

O jogo original tinha 4 blocos de código quase idênticos (meteoro1..4) só
mudando o nome das variáveis. Aqui é uma classe só, reaproveitada 4 vezes:
`variance_sign` reproduz a diferença de comportamento entre eles (meteoro1
tem velocidade fixa, meteoro2/4 variam pra mais, meteoro3 varia pra menos).
"""

import random

import pygame

import settings
from src.animation import Animation
from src.effects import build_explosion_frames
from src.utils import pick_x

EXPLOSION_FRAME_DURATION = 0.045


class Meteor(pygame.sprite.Sprite):
    def __init__(self, assets, image_path, start_x, start_y, variance_sign=0):
        super().__init__()
        self._meteor_image = assets.image(image_path)
        self.image = self._meteor_image
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.pos = pygame.Vector2(start_x, start_y)

        self.variance_sign = variance_sign
        self.variance = 0.0
        self._roll_variance()

        self.exploding = False
        self.explosion_anim = None
        self._respawn_kind = None
        self._respawn_positions = None

    def _roll_variance(self):
        if self.variance_sign > 0:
            self.variance = random.uniform(0, settings.METEOR_VARIANCE_PLUS_MAX)
        elif self.variance_sign < 0:
            self.variance = -random.uniform(0, settings.METEOR_VARIANCE_DOWN_MAX)
        else:
            self.variance = 0.0

    @property
    def speed(self):
        return settings.METEOR_SPEED + self.variance

    def reset(self, x, y):
        """Recoloca o meteoro numa posição, cancelando qualquer explosão em andamento."""
        self.exploding = False
        self.pos.update(x, y)
        self.image = self._meteor_image
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))

    def update(self, dt, recent_x_positions):
        if self.exploding:
            self.explosion_anim.update(dt)
            self.image = self.explosion_anim.current_frame()
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.explosion_anim.finished:
                self._finish_explosion()
            return

        self.pos.y += self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > settings.SCREEN_H:
            self._respawn_from_bottom(recent_x_positions)

    def _respawn_from_bottom(self, recent_x_positions):
        self._roll_variance()
        self.pos.y = 10
        self.pos.x = pick_x(recent_x_positions, settings.SCREEN_W, self.image.get_width(), max_history=100)
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def hit_by_laser(self, recent_x_positions):
        """Atingido pelo laser: só ele explode e reaparece numa posição nova."""
        self._begin_explosion(kind="laser", recent_x_positions=recent_x_positions)

    def hit_by_ship(self):
        """A nave bateu nele: explode e reaparece mais longe, dando um respiro pro jogador."""
        self._begin_explosion(kind="ship")

    def _begin_explosion(self, kind, recent_x_positions=None):
        if self.exploding:
            return
        self.exploding = True
        self._respawn_kind = kind
        self._respawn_positions = recent_x_positions
        self.explosion_anim = Animation(build_explosion_frames(), EXPLOSION_FRAME_DURATION, loop=False)

    def _finish_explosion(self):
        self.exploding = False
        self.image = self._meteor_image
        if self._respawn_kind == "laser":
            self.pos.y = -150
            self.pos.x = pick_x(self._respawn_positions, settings.SCREEN_W, self.image.get_width(), max_history=100)
        else:  # "ship"
            self.pos.y = -410
        self.rect = self.image.get_rect(topleft=(round(self.pos.x), round(self.pos.y)))
