import pygame
from src import config
from src.assets import Assets
from src.models.model import GameModel

class Renderer:

    def __init__(self, screen: pygame.Surface, assets: Assets) -> None:
  
        self.screen = screen
        self.assets = assets
        self.splash_rect = self.assets.splash.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        )

    def draw(self, model: GameModel) -> None:
        self.screen.blit(self.assets.nebula, (0, 0))

        x_offset = int(model.debris_offset)
        self.screen.blit(self.assets.debris, (x_offset, 0))
        self.screen.blit(self.assets.debris, (x_offset - config.SCREEN_WIDTH, 0))

        if model.in_play:
            for missile in model.missiles:
                rect = self.assets.missile.get_rect(center=missile.pos)
                self.screen.blit(self.assets.missile, rect)

            for asteroid in model.asteroids:
                rotated_ast = pygame.transform.rotate(self.assets.asteroid, -asteroid.angle)
                rect = rotated_ast.get_rect(center=asteroid.pos)
                self.screen.blit(rotated_ast, rect)

            ship_img = (
                self.assets.ship_thrust if model.ship.thrust else self.assets.ship_idle
            )
            rotated_ship = pygame.transform.rotate(ship_img, -model.ship.angle)
            ship_rect = rotated_ship.get_rect(center=model.ship.pos)
            self.screen.blit(rotated_ship, ship_rect)

        for exp in model.explosions:
            tile = self.assets.explosion_tiles[exp.frame]
            self.screen.blit(tile, tile.get_rect(center=exp.pos))

        if not model.in_play:
            self.screen.blit(self.assets.splash, self.splash_rect)

        self._draw_hud(model)

        pygame.display.flip()

    def _draw_hud(self, model: GameModel) -> None:
        lives_surf = self.assets.hud_font.render(
            f"Lives: {model.lives}", True, config.TEXT_COLOR
        )
        score_surf = self.assets.hud_font.render(
            f"Score: {model.score}", True, config.TEXT_COLOR
        )
        self.screen.blit(lives_surf, (60, 15))
        self.screen.blit(
            score_surf, (config.SCREEN_WIDTH - score_surf.get_width() - 60, 15)
        )
