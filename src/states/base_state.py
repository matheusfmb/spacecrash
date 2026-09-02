"""Interface comum das telas do jogo (menu, jogando, game over)."""


class State:
    def __init__(self, game):
        self.game = game

    def enter(self, **kwargs):
        """Chamado quando o jogo entra nessa tela."""

    def exit(self):
        """Chamado quando o jogo sai dessa tela."""

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
