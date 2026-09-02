"""A nave controlada pelo jogador."""

import pygame

import settings
from src.animation import Animation
from src.effects import build_thrust_frames


class Ship(pygame.sprite.Sprite):
    def __init__(self, assets):
        super().__init__()
        self.image = assets.image(settings.SHIP_IMAGE)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(settings.SHIP_START_X, settings.SHIP_START_Y)

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # animação do propulsor, desenhada atrás da nave enquanto ela se move
        self.thrust_anim = Animation(build_thrust_frames(), frame_duration=0.06, loop=True)

        # "pisca" de dano: fica alternando visível/invisível por um tempo
        # depois de levar um hit que não foi fatal
        self.visible = True
        self.flashing = False
        self.flash_timer = 0.0

        self._sync_rect()

    def reset(self):
        self.pos.update(settings.SHIP_START_X, settings.SHIP_START_Y)
        self.moving_up = self.moving_down = self.moving_left = self.moving_right = False
        self.thrust_anim.reset()
        self.visible = True
        self.flashing = False
        self.flash_timer = 0.0
        self._sync_rect()

    def _sync_rect(self):
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def start_hit_flash(self):
        self.flashing = True
        self.flash_timer = 0.0
        self.visible = False

    def handle_event(self, event):
        pressed = event.type == pygame.KEYDOWN
        released = event.type == pygame.KEYUP
        if not (pressed or released):
            return
        if event.key == pygame.K_UP:
            self.moving_up = pressed
        elif event.key == pygame.K_DOWN:
            self.moving_down = pressed
        elif event.key == pygame.K_LEFT:
            self.moving_left = pressed
        elif event.key == pygame.K_RIGHT:
            self.moving_right = pressed

    @property
    def is_moving(self):
        return self.moving_up or self.moving_down or self.moving_left or self.moving_right

    def update(self, dt):
        if self.flashing:
            self._update_flash(dt)

        if self.moving_up:
            self.pos.y -= settings.SHIP_SPEED * dt
        if self.moving_down:
            self.pos.y += settings.SHIP_SPEED * dt
        if self.moving_left:
            self.pos.x -= settings.SHIP_SPEED * dt
        if self.moving_right:
            self.pos.x += settings.SHIP_SPEED * dt

        self.pos.x = max(settings.SHIP_X_MIN, min(settings.SHIP_X_MAX, self.pos.x))
        self.pos.y = max(settings.SHIP_Y_MIN, min(settings.SHIP_Y_MAX, self.pos.y))
        self._sync_rect()

        if self.is_moving:
            self.thrust_anim.update(dt)

    def _update_flash(self, dt):
        self.flash_timer += dt
        if self.flash_timer >= settings.SHIP_FLASH_DURATION:
            self.flashing = False
            self.visible = True
        else:
            step = int(self.flash_timer / settings.SHIP_FLASH_INTERVAL)
            self.visible = step % 2 == 0

    def draw(self, surface):
        if not self.visible:
            return
        if self.is_moving:
            frame = self.thrust_anim.current_frame()
            flame_rect = frame.get_rect(midtop=(self.rect.centerx, self.rect.bottom - 8))
            surface.blit(frame, flame_rect)
        surface.blit(self.image, self.rect)
