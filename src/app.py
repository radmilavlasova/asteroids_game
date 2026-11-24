import pygame
from src import config
from src.assets import Assets
from src.models.model import GameModel
from src.renderers.renderer import Renderer


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Asteroids")
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.model.in_play and self.renderer.splash_rect.collidepoint(event.pos):
                    self.model.start_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.model.fire_missile()

    def _update(self) -> None:
        keys = pygame.key.get_pressed()
        turn_dir = 0
        if keys[pygame.K_LEFT]:
            turn_dir -= 1
        if keys[pygame.K_RIGHT]:
            turn_dir += 1

        thrusting = bool(keys[pygame.K_UP])
        self.model.update(turn_dir, thrusting, pygame.time.get_ticks())
