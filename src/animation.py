"""Animação simples baseada em uma lista de frames (imagens)."""


class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.index = 0
        self.timer = 0.0
        self.finished = False

    def update(self, dt):
        if self.finished:
            return
        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.finished = True
                    break

    def current_frame(self):
        return self.frames[self.index]

    def reset(self):
        self.index = 0
        self.timer = 0.0
        self.finished = False
