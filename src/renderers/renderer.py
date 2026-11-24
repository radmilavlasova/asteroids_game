import pygame
from src import config
from src.assets import Assets
from src.models.model import GameModel


class Renderer:

    def __init__(self, screen: pygame.Surface, assets: Assets) -> None:
        self.screen = screen
        self.assets = assets

    def draw(self, model: GameModel) -> None:
        self.screen.fill(config.BLACK)

        pygame.draw.rect(self.screen, config.PLAYER_COLOR, model.player.rect)

        for bullet in model.bullets:
            pygame.draw.rect(self.screen, config.BULLET_COLOR, bullet.rect)

        for asteroid in model.asteroids:
            pygame.draw.rect(self.screen, config.ASTEROID_COLOR, asteroid.rect)

        self._draw_hud(model)

        if model.game_over:
            self._draw_game_over(model.score)

        pygame.display.flip()

    def _draw_hud(self, model: GameModel) -> None:
        score_surf = self.assets.hud_font.render(
            f"Счет: {model.score}", True, config.WHITE
        )
        lives_surf = self.assets.hud_font.render(
            f"Жизни: {model.lives}", True, config.WHITE
        )
        self.screen.blit(score_surf, (15, 15))
        self.screen.blit(
            lives_surf, (config.SCREEN_WIDTH - lives_surf.get_width() - 15, 15)
        )

    def _draw_game_over(self, final_score: int) -> None:
        overlay = pygame.Surface(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))

        title = self.assets.title_font.render("ИГРА ОКОНЧЕНА", True, config.ASTEROID_COLOR)
        score_text = self.assets.hud_font.render(
            f"Итоговый счет: {final_score}", True, config.WHITE
        )
        hint = self.assets.hud_font.render(
            "Нажмите R для рестарта или ESC для выхода", True, config.WHITE
        )

        cx = config.SCREEN_WIDTH // 2
        cy = config.SCREEN_HEIGHT // 2
        self.screen.blit(title, title.get_rect(center=(cx, cy - 45)))
        self.screen.blit(score_text, score_text.get_rect(center=(cx, cy + 5)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 50)))
