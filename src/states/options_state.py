"""
Menu de opções (acessado do menu principal, tecla O): um modal com o
AudioMenuPanel por cima do menu, que continua visível atrás.
"""

import pygame

import settings
from src.audio_menu import AudioMenuPanel
from src.states.base_state import State


class OptionsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = game.assets.image(settings.MENU_IMAGE, convert_alpha=False)
        self.panel = AudioMenuPanel(game)

    def enter(self, **kwargs):
        self.panel.reset()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.panel.handle_key(event.key):
            self.game.change_state("menu")

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.panel.draw(surface)
