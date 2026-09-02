"""Classe principal: janela- loop do jogo e troca de telas (estados)."""

import pygame

import settings
from src.assets import AssetManager
from src.audio import AudioSettings
from src.states.gameover_state import GameOverState
from src.states.menu_state import MenuState
from src.states.options_state import OptionsState
from src.states.playing_state import PlayingState


class Game:
    def __init__(self):
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.running = True

        self.assets = AssetManager()

        # volumes salvos de uma sessão anterior (ou os padrões, se não houver save)
        self.audio = AudioSettings.load()

        self.assets.load_music(settings.MUSIC_START)
        self.audio.apply_music_volume()
        pygame.mixer.music.play(-1)

        # cada tela é criada uma vez só
        self.states = {
            "menu": MenuState(self),
            "playing": PlayingState(self),
            "gameover": GameOverState(self),
            "options": OptionsState(self),
        }
        self.state = self.states["menu"]
        self.state.enter()

        # fade preto usado nas trocas de tela
        self._fade_surface = pygame.Surface((settings.SCREEN_W, settings.SCREEN_H))
        self._fade_surface.fill((0, 0, 0))
        self.fade_alpha = 0

    def change_state(self, name, **kwargs):
        self.state.exit()
        self.state = self.states[name]
        self.state.enter(**kwargs)
        self.fade_alpha = 255

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS_CAP) / 1000.0
            self._handle_events()
            self.state.update(dt)
            self._update_fade(dt)

            self.state.draw(self.screen)
            self._draw_fade(self.screen)
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.state.handle_event(event)

    def _update_fade(self, dt):
        if self.fade_alpha > 0:
            step = 255 * dt / settings.FADE_DURATION
            self.fade_alpha = max(0, self.fade_alpha - step)

    def _draw_fade(self, surface):
        if self.fade_alpha > 0:
            self._fade_surface.set_alpha(int(self.fade_alpha))
            surface.blit(self._fade_surface, (0, 0))
