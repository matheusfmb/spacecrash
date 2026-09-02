"""
Painel de ajuste de volume
"""

import pygame

import settings

BAR_BG_COLOR = (55, 58, 90)
SELECTED_COLOR = (255, 210, 90)
BAR_HEIGHT = 16
PANEL_MARGIN = 24

CLOSE_KEYS = (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_o, pygame.K_BACKSPACE)


class AudioMenuPanel:
    def __init__(self, game):
        self.game = game
        self.title_font = game.assets.font(settings.FONT_PATH, 20)
        self.row_font = game.assets.font(settings.FONT_PATH, settings.CREDIT_FONT_SIZE)
        self.hint_font = game.assets.font(settings.FONT_PATH, settings.OPTIONS_HINT_FONT_SIZE)
        self.selected = 0  # 0 = música, 1 = efeitos (SFX)

        self.panel_rect = pygame.Rect(0, 0, settings.MODAL_W, settings.MODAL_H)
        self.panel_rect.center = (settings.SCREEN_W // 2, settings.SCREEN_H // 2)
        self.panel = pygame.Surface(self.panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.panel,
            (*settings.MODAL_COLOR, settings.MODAL_OPACITY),
            self.panel.get_rect(),
            border_radius=16,
        )

    def reset(self):
        self.selected = 0

    def handle_key(self, key):
        """Processa uma tecla; retorna True se o painel deve ser fechado."""
        if key in CLOSE_KEYS:
            return True
        if key in (pygame.K_UP, pygame.K_DOWN):
            self.selected = 1 - self.selected
        elif key == pygame.K_LEFT:
            self._adjust(-settings.VOLUME_STEP)
        elif key == pygame.K_RIGHT:
            self._adjust(settings.VOLUME_STEP)
        return False

    def _adjust(self, delta):
        audio = self.game.audio
        if self.selected == 0:
            audio.adjust_music_volume(delta)
        else:
            audio.adjust_sfx_volume(delta)
        audio.save()

    def draw(self, surface):
        surface.blit(self.panel, self.panel_rect.topleft)
        px, py, pw = self.panel_rect.x, self.panel_rect.y, self.panel_rect.width

        title = self.title_font.render("AUDIO", True, settings.WHITE_TEXT)
        surface.blit(title, title.get_rect(centerx=px + pw // 2, y=py + PANEL_MARGIN))

        self._draw_row(surface, x=px + PANEL_MARGIN, y=py + 90, width=pw - PANEL_MARGIN * 2,
                        label="MUSICA", value=self.game.audio.music_volume, row=0)
        self._draw_row(surface, x=px + PANEL_MARGIN, y=py + 165, width=pw - PANEL_MARGIN * 2,
                        label="EFEITOS", value=self.game.audio.sfx_volume, row=1)

        hint_line1 = self.hint_font.render("SETAS AJUSTAM", True, settings.WHITE_TEXT)
        hint_line2 = self.hint_font.render("ENTER VOLTA", True, settings.WHITE_TEXT)
        hint_y = py + settings.MODAL_H - PANEL_MARGIN - 24
        surface.blit(hint_line1, hint_line1.get_rect(centerx=px + pw // 2, y=hint_y))
        surface.blit(hint_line2, hint_line2.get_rect(centerx=px + pw // 2, y=hint_y + 14))

    def _draw_row(self, surface, x, y, width, label, value, row):
        selected = self.selected == row
        color = SELECTED_COLOR if selected else settings.WHITE_TEXT
        prefix = "> " if selected else "  "

        label_surf = self.row_font.render(f"{prefix}{label}  {round(value * 100)}%", True, color)
        surface.blit(label_surf, (x, y))

        bar_y = y + 26
        pygame.draw.rect(surface, BAR_BG_COLOR, (x, bar_y, width, BAR_HEIGHT), border_radius=6)
        fill_width = round(width * value)
        if fill_width > 0:
            pygame.draw.rect(surface, color, (x, bar_y, fill_width, BAR_HEIGHT), border_radius=6)
