import pygame

class Assets:
    def __init__(self) -> None:
        self.hud_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 44, bold=True)
