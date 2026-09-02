"""
Tela inicial
"""

import pygame

import settings
from src.states.base_state import State

ICON_MARGIN = 12
ICON_GAP = 10


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = game.assets.image(settings.MENU_IMAGE, convert_alpha=False)
        self.hint_font = game.assets.font(settings.FONT_PATH, settings.AUDIO_HINT_FONT_SIZE)
        self.title_font = game.assets.font(settings.FONT_PATH, 20)
        self.line_font = game.assets.font(settings.FONT_PATH, settings.OPTIONS_HINT_FONT_SIZE)

        self.audio_icon = self._load_icon(game, settings.AUDIO_ICON_IMAGE)
        self.audio_icon_rect = self.audio_icon.get_rect(
            bottomright=(settings.SCREEN_W - ICON_MARGIN, settings.SCREEN_H - ICON_MARGIN)
        )

        self.controls_icon = self._load_icon(game, settings.JOYSTICK_IMAGE)
        self.controls_icon_rect = self.controls_icon.get_rect(
            bottomright=(settings.SCREEN_W - ICON_MARGIN, self.audio_icon_rect.top - ICON_GAP)
        )

        self.showing_controls = False
        self.controls_panel_rect = pygame.Rect(0, 0, settings.CONTROLS_MODAL_W, settings.CONTROLS_MODAL_H)
        self.controls_panel_rect.center = (settings.SCREEN_W // 2, settings.SCREEN_H // 2)
        self.controls_panel = pygame.Surface(self.controls_panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.controls_panel,
            (*settings.MODAL_COLOR, settings.MODAL_OPACITY),
            self.controls_panel.get_rect(),
            border_radius=16,
        )

    @staticmethod
    def _load_icon(game, path):
        raw = game.assets.image(path)
        return pygame.transform.smoothscale(raw, (settings.AUDIO_ICON_SIZE, settings.AUDIO_ICON_SIZE))

    def enter(self, **kwargs):
        self.showing_controls = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.showing_controls:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_c):
                self.showing_controls = False
            return

        if event.key == pygame.K_RETURN:
            self.game.change_state("playing")
        elif event.key == pygame.K_o:
            self.game.change_state("options")
        elif event.key == pygame.K_c:
            self.showing_controls = True

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self._draw_icon_with_hint(surface, self.audio_icon, self.audio_icon_rect, settings.AUDIO_HINT_TEXT)
        self._draw_icon_with_hint(surface, self.controls_icon, self.controls_icon_rect, settings.CONTROLS_HINT_TEXT)

        if self.showing_controls:
            self._draw_controls_modal(surface)

    def _draw_icon_with_hint(self, surface, icon, icon_rect, text):
        surface.blit(icon, icon_rect)
        hint = self.hint_font.render(text, True, settings.WHITE_TEXT)
        hint_rect = hint.get_rect(bottomright=(icon_rect.left - 6, icon_rect.bottom - 2))
        surface.blit(hint, hint_rect)

    def _draw_controls_modal(self, surface):
        surface.blit(self.controls_panel, self.controls_panel_rect.topleft)
        px, py, pw = self.controls_panel_rect.x, self.controls_panel_rect.y, self.controls_panel_rect.width

        title = self.title_font.render(settings.CONTROLS_MODAL_TITLE, True, settings.WHITE_TEXT)
        surface.blit(title, title.get_rect(centerx=px + pw // 2, y=py + 24))

        line_y = py + 74
        for line in settings.CONTROLS_LINES:
            line_surf = self.line_font.render(line, True, settings.WHITE_TEXT)
            surface.blit(line_surf, (px + 24, line_y))
            line_y += 30

        hint = self.line_font.render("ENTER OU ESC: FECHAR", True, settings.WHITE_TEXT)
        surface.blit(hint, hint.get_rect(centerx=px + pw // 2, y=py + settings.CONTROLS_MODAL_H - 32))
