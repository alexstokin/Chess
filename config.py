import pygame
import os

from sound import Sound

class Config:
    def __init__(self):
        self.font = pygame.font.SysFont('JetBrains Mono', 20, bold=True)
        self.move_sound = Sound(os.path.join('Scena/chess/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('Scena/chess/sounds/capture.wav'))
