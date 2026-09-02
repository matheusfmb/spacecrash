"""
Geração de frames de animação para efeitos visuais (propulsor, explosão, moeda girando).
"""

import pygame


def build_thrust_frames():
    """3 frames de uma chama de propulsor, variando de tamanho (flicker)."""
    frames = []
    heights = (14, 20, 16)
    for height in heights:
        width = 10
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(
            surface,
            (255, 200, 60, 230),
            [(0, 0), (width, 0), (width // 2, height)],
        )
        pygame.draw.polygon(
            surface,
            (255, 240, 180, 230),
            [(width * 0.25, 0), (width * 0.75, 0), (width // 2, height * 0.6)],
        )
        frames.append(surface)
    return frames


def build_explosion_frames(max_radius=26):
    """Frames de um círculo se expandindo e desbotando, tipo explosão."""
    frames = []
    steps = 6
    size = max_radius * 2
    for step in range(steps):
        progress = step / (steps - 1)
        radius = int(max_radius * (0.3 + 0.7 * progress))
        alpha = int(255 * (1 - progress))
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(surface, (255, 140, 30, alpha), center, radius)
        pygame.draw.circle(surface, (255, 220, 120, alpha), center, max(1, radius // 2))
        frames.append(surface)
    return frames


def build_coin_spin_frames(coin_image):
    """
    Simula a moeda girando
    """
    width, height = coin_image.get_size()
    widths = (width, int(width * 0.6), int(width * 0.15), int(width * 0.6))
    frames = []
    for w in widths:
        w = max(2, w)
        frame = pygame.transform.smoothscale(coin_image, (w, height))
        frames.append(frame)
    return frames
