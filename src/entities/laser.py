"""
O "tiro" da nave.

No jogo original não existe uma tecla de atirar: existe um único laser que
sobe continuamente e, quando some bem acima da tela, reaparece atrás da
nave e recomeça a subir. Esse comportamento é mantido de propósito — trocar
para múltiplos tiros disparados por tecla é uma melhoria futura, fora do
escopo deste refactor.
"""

import pygame

import settings


class Laser(pygame.sprite.Sprite):
    def __init__(self, assets, ship):
        super().__init__()
        self.image = assets.image(settings.LASER_IMAGE)
        self.rect = self.image.get_rect()
        self.ship = ship
        self.pos = pygame.Vector2(0, 0)
        self.reset()

    def reset(self):
        self.pos.update(self.ship.rect.x + 25, self.ship.rect.y - 50)
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def update(self, dt):
        self.pos.y -= settings.LASER_SPEED * dt
        if self.pos.y < -1000:
            self.reset()
        else:
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
