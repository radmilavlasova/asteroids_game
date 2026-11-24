import pygame
from src import config
from src.assets import Assets
from src.models.model import GameModel
from src.renderers.renderer import Renderer

class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Простые астероиды — Лабораторная работа №4")
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.model = GameModel()
        self.renderer = Renderer(self.screen, self.assets)
        self.running = True

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._update()
            self.renderer.draw(self.model)
            self.clock.tick(config.FPS)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.model.shoot()
                elif event.key == pygame.K_r and self.model.game_over:
                    self.model.reset()

    def _update(self) -> None:
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1

        self.model.update(direction, pygame.time.get_ticks())
