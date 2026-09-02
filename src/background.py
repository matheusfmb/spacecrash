"""Fundo com efeito de rolagem contínua (parallax simples)."""


class Parallax:
    def __init__(self, image, screen_height, speed_px_s):
        self.image = image
        self.height = screen_height
        self.speed = speed_px_s
        self.offset = 0.0

    def update(self, dt):
        self.offset = (self.offset + self.speed * dt) % self.height

    def draw(self, surface):
        surface.blit(self.image, (0, self.offset))
        surface.blit(self.image, (0, self.offset - self.height))
