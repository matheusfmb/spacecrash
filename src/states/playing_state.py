"""
Tela principal do jogo playing state
"""

import random

import pygame

import settings
from src.animation import Animation
from src.audio_menu import AudioMenuPanel
from src.background import Parallax
from src.effects import build_explosion_frames
from src.entities.coin import Coin
from src.entities.laser import Laser
from src.entities.meteor import Meteor
from src.entities.ship import Ship
from src.hud import Hud
from src.states.base_state import State


class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
        assets = game.assets

        self.background = Parallax(
            assets.image(settings.BACKGROUND_IMAGE, convert_alpha=False),
            settings.SCREEN_H,
            settings.BACKGROUND_SPEED,
        )
        self.pause_icon = assets.image(settings.PAUSE_IMAGE)
        self.pause_icon_rect = self.pause_icon.get_rect(topright=(settings.SCREEN_W, 10))

        return_icon_raw = assets.image(settings.RETURN_ICON_IMAGE)
        self.quit_icon = pygame.transform.smoothscale(
            return_icon_raw, (self.pause_icon.get_height(), self.pause_icon.get_height())
        )
        self.quit_icon_rect = self.quit_icon.get_rect(
            midright=(self.pause_icon_rect.left - settings.QUIT_ICON_MARGIN, self.pause_icon_rect.centery)
        )

        self.confirm_title_font = assets.font(settings.FONT_PATH, 18)
        self.confirm_hint_font = assets.font(settings.FONT_PATH, settings.OPTIONS_HINT_FONT_SIZE)
        self.confirm_panel_rect = pygame.Rect(0, 0, settings.QUIT_MODAL_W, settings.QUIT_MODAL_H)
        self.confirm_panel_rect.center = (settings.SCREEN_W // 2, settings.SCREEN_H // 2)
        self.confirm_panel = pygame.Surface(self.confirm_panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.confirm_panel,
            (*settings.MODAL_COLOR, settings.MODAL_OPACITY),
            self.confirm_panel.get_rect(),
            border_radius=16,
        )
        self.confirming_quit = False

        self.audio_menu = AudioMenuPanel(game)
        self.showing_audio_menu = False

        self.hud = Hud(assets)
        self.meteor_hit_sfx = assets.sound(settings.SOUND_METEOR_HIT)
        self.coin_sfx = assets.sound(settings.SOUND_COIN)
        game.audio.register_sfx(self.meteor_hit_sfx, settings.METEOR_HIT_SFX_VOLUME)
        game.audio.register_sfx(self.coin_sfx, settings.COIN_SFX_VOLUME)

        self.ship = Ship(assets)
        self.laser = Laser(assets, self.ship)
        self.coin = Coin(assets)

        # meteoro1 tem velocidade fixa; meteoro2/4 variam pra mais; meteoro3 varia pra menos
        # (o 4º só entra em jogo quando o score bate METEOR4_UNLOCK_SCORE)
        self._meteor1 = self._make_meteor(assets, 0, variance_sign=0)
        self._meteor2 = self._make_meteor(assets, 1, variance_sign=1)
        self._meteor3 = self._make_meteor(assets, 2, variance_sign=-1)
        self._bonus_meteor = self._make_meteor(assets, 3, variance_sign=1)
        self.meteors = pygame.sprite.Group(self._meteor1, self._meteor2, self._meteor3)
        self.recent_meteor_x = []

        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.paused = False
        self.confirming_quit = False
        self.showing_audio_menu = False
        self.dying = False
        self.death_anim = None

    @staticmethod
    def _make_meteor(assets, image_index, variance_sign):
        start_x = random.randrange(0, settings.SCREEN_W - 40)
        return Meteor(assets, settings.METEOR_IMAGES[image_index], start_x, 10, variance_sign)

    def enter(self, **kwargs):
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.paused = False
        self.confirming_quit = False
        self.showing_audio_menu = False
        self.dying = False
        self.death_anim = None
        self.ship.reset()
        self.laser.reset()
        self.coin.respawn(at_top=True)
        self.recent_meteor_x = []

        for meteor in (self._meteor1, self._meteor2, self._meteor3, self._bonus_meteor):
            meteor.reset(random.randrange(0, settings.SCREEN_W - 40), 10)

        self.meteors = pygame.sprite.Group(self._meteor1, self._meteor2, self._meteor3)

    def handle_event(self, event):
        if self.dying:
            return  # nave explodindo: ignora entrada até a animação acabar

        if event.type == pygame.KEYDOWN:
            if self.confirming_quit:
                self._handle_confirm_quit_key(event.key)
            elif self.showing_audio_menu:
                if self.audio_menu.handle_key(event.key):
                    self.showing_audio_menu = False
            elif event.key == pygame.K_BACKSPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_q and self.paused:
                self.confirming_quit = True
            elif event.key == pygame.K_o and self.paused:
                self.audio_menu.reset()
                self.showing_audio_menu = True

        self.ship.handle_event(event)

    def _handle_confirm_quit_key(self, key):
        if key == pygame.K_RETURN:
            self.confirming_quit = False
            self.game.change_state("menu")
        elif key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            # cancela: fecha o modal e volta pro pause como estava
            self.confirming_quit = False

    def update(self, dt):
        self.background.update(dt)

        if self.dying:
            self.death_anim.update(dt)
            if self.death_anim.finished:
                self.dying = False
                self.game.change_state("gameover", score=self.score)
            return

        if self.paused:
            return

        if self.score >= settings.METEOR4_UNLOCK_SCORE:
            self.meteors.add(self._bonus_meteor)

        self.ship.update(dt)
        self.laser.update(dt)
        self.coin.update(dt)
        for meteor in self.meteors:
            meteor.update(dt, self.recent_meteor_x)

        self._handle_collisions()

    def _handle_collisions(self):
        hit_ship = any(
            not meteor.exploding and self.ship.rect.colliderect(meteor.rect)
            for meteor in self.meteors
        )
        if hit_ship:
            self._on_ship_hit()

        if self.ship.rect.colliderect(self.coin.rect):
            self._on_coin_collected()

        for meteor in self.meteors:
            if not meteor.exploding and self.laser.rect.colliderect(meteor.rect):
                meteor.hit_by_laser(self.recent_meteor_x)

    def _on_ship_hit(self):
        self.lives -= 1
        self.meteor_hit_sfx.play()
        for meteor in self.meteors:
            meteor.hit_by_ship()
        self.coin.respawn()
        if self.lives <= 0:
            self._start_ship_death()
        else:
            self.ship.start_hit_flash()

    def _start_ship_death(self):
        self.dying = True
        self.death_anim = Animation(
            build_explosion_frames(max_radius=settings.SHIP_DEATH_EXPLOSION_RADIUS),
            frame_duration=settings.SHIP_DEATH_FRAME_DURATION,
            loop=False,
        )

    def _on_coin_collected(self):
        self.coin.respawn()
        self.score += 1
        self.coin_sfx.play()

    def draw(self, surface):
        self.background.draw(surface)

        if self.dying:
            frame = self.death_anim.current_frame()
            surface.blit(frame, frame.get_rect(center=self.ship.rect.center))
        else:
            self.ship.draw(surface)

        surface.blit(self.laser.image, self.laser.rect)
        self.meteors.draw(surface)
        surface.blit(self.coin.image, self.coin.rect)
        self.hud.draw(surface, self.score, self.lives)
        if self.paused:
            surface.blit(self.pause_icon, self.pause_icon_rect)
            surface.blit(self.quit_icon, self.quit_icon_rect)
        if self.confirming_quit:
            self._draw_confirm_quit_modal(surface)
        elif self.showing_audio_menu:
            self.audio_menu.draw(surface)

    def _draw_confirm_quit_modal(self, surface):
        surface.blit(self.confirm_panel, self.confirm_panel_rect.topleft)

        px, py, pw = self.confirm_panel_rect.x, self.confirm_panel_rect.y, self.confirm_panel_rect.width

        title = self.confirm_title_font.render(settings.QUIT_CONFIRM_TITLE, True, settings.WHITE_TEXT)
        surface.blit(title, title.get_rect(centerx=px + pw // 2, y=py + 30))

        hint = self.confirm_hint_font.render(settings.QUIT_CONFIRM_HINT, True, settings.WHITE_TEXT)
        surface.blit(hint, hint.get_rect(centerx=px + pw // 2, y=py + settings.QUIT_MODAL_H - 40))
