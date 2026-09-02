"""Funções pequenas reaproveitadas por mais de uma entidade."""

import random

#Função da pick em uma posição aleatória no eixo X, evitando colisão com outras entidades
def pick_x(taken_positions, screen_width, sprite_width, max_history):
    x = random.randrange(0, screen_width - sprite_width)
    if x in taken_positions:
        x = random.randrange(0, screen_width - sprite_width)
    else:
        taken_positions.append(x)
        if len(taken_positions) > max_history:
            taken_positions.clear()
    return x
