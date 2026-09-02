"""Tela de game oveR."""

import pygame

import settings
from src.states.base_state import State


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        assets = game.assets
        self.background = assets.image(settings.GAMEOVER_IMAGE, convert_alpha=False)
        self.font = assets.font(settings.FONT_PATH, settings.FONT_SIZE)
        self.credit_font = assets.font(settings.FONT_PATH, settings.CREDIT_FONT_SIZE)
        self.death_sfx = assets.sound(settings.SOUND_GAMEOVER)
        game.audio.register_sfx(self.death_sfx, settings.GAMEOVER_SFX_VOLUME)
        self.score = 0

    def enter(self, score=0, **kwargs):
        self.score = score
        pygame.mixer.music.stop()
        self.death_sfx.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mixer.music.play(-1)
            self.game.change_state("menu")

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        text = self.font.render(f"score: {self.score}", True, settings.WHITE_TEXT)
        surface.blit(text, (100, 400))

        credit = self.credit_font.render(settings.CREDIT_TEXT, True, settings.WHITE_TEXT)
        credit_rect = credit.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H - 30))
        surface.blit(credit, credit_rect)
