"""Placar de score e indicador de vidas restantes."""

import settings

class Hud:
    def __init__(self, assets):
        self.font = assets.font(settings.FONT_PATH, settings.FONT_SIZE)
        self.life_sprites = [assets.image(path) for path in settings.LIFE_IMAGES]

    def draw(self, surface, score, lives):
        text = self.font.render(f"score: {score}", True, settings.WHITE_TEXT)
        surface.blit(text, (10, 10))

        # vidas=3 -> vida1.png (3 corações) ... vidas=0 -> vida4.png (0 corações)
        index = max(0, min(3, settings.STARTING_LIVES - lives))
        surface.blit(self.life_sprites[index], (20, 40))
