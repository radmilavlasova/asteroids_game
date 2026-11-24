import math
import random
from typing import List
import pygame
from src import config


class Assets:

    def __init__(self) -> None:
        self.hud_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.nebula = self._create_nebula()
        self.debris = self._create_debris()
        self.ship_idle = self._create_ship(thrust=False)
        self.ship_thrust = self._create_ship(thrust=True)
        self.asteroid = self._create_asteroid()
        self.missile = self._create_missile()
        self.explosion_tiles = self._create_explosion_tileset()
        self.splash = self._create_splash()

    def _create_nebula(self) -> pygame.Surface:
        surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        surf.fill((10, 8, 18))
        rng = random.Random(42)

        nebula_colors = [(95, 35, 25, 28), (35, 45, 95, 28), (110, 50, 20, 22)]
        for _ in range(45):
            cloud = pygame.Surface((260, 260), pygame.SRCALPHA)
            color = rng.choice(nebula_colors)
            pygame.draw.circle(cloud, color, (130, 130), rng.randint(60, 125))
            surf.blit(cloud, (rng.randint(-100, config.SCREEN_WIDTH), rng.randint(-100, config.SCREEN_HEIGHT)))

        cx, cy = config.SCREEN_WIDTH // 2 + 40, config.SCREEN_HEIGHT // 2 - 20
        for r, alpha in [(55, 25), (30, 60), (14, 140), (6, 255)]:
            glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (140, 210, 255, alpha), (r, r), r)
            surf.blit(glow, (cx - r, cy - r))

        for _ in range(180):
            x = rng.randint(0, config.SCREEN_WIDTH - 1)
            y = rng.randint(0, config.SCREEN_HEIGHT - 1)
            brightness = rng.randint(130, 255)
            pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), rng.choice([1, 1, 2]))

        return surf

    def _create_debris(self) -> pygame.Surface:
        surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        rng = random.Random(99)
        for _ in range(65):
            x = rng.randint(15, config.SCREEN_WIDTH - 15)
            y = rng.randint(15, config.SCREEN_HEIGHT - 15)
            r = rng.randint(3, 8)
            color = (rng.randint(110, 160), rng.randint(105, 145), rng.randint(95, 130), 145)
            pygame.draw.circle(surf, color, (x, y), r)
            pygame.draw.circle(surf, (70, 65, 60, 160), (x - 1, y - 1), max(1, r // 2))
        return surf

    def _create_ship(self, thrust: bool) -> pygame.Surface:
        size = 90
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        c = size // 2

        if thrust:
            pygame.draw.polygon(surf, (255, 100, 20), [(c - 18, c - 10), (c - 42, c), (c - 18, c + 10)])
            pygame.draw.polygon(surf, (255, 230, 90), [(c - 18, c - 5), (c - 32, c), (c - 18, c + 5)])

        pygame.draw.polygon(
            surf, (150, 160, 175),
            [(c + 32, c), (c - 18, c - 28), (c - 10, c), (c - 18, c + 28)],
        )
        pygame.draw.polygon(
            surf, (230, 235, 245),
            [(c + 32, c), (c - 10, c - 15), (c - 20, c), (c - 10, c + 15)],
        )

        pygame.draw.line(surf, (210, 45, 45), (c - 12, c - 20), (c + 8, c - 8), 3)
        pygame.draw.line(surf, (210, 45, 45), (c - 12, c + 20), (c + 8, c + 8), 3)
        pygame.draw.ellipse(surf, (45, 160, 230), (c - 2, c - 5, 16, 10))
        return surf

    def _create_asteroid(self) -> pygame.Surface:
        r = config.ASTEROID_RADIUS
        size = r * 2 + 4
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        c = size // 2
        rng = random.Random(7)

        points = []
        for i in range(16):
            ang = (2 * math.pi * i) / 16
            rad = r * rng.uniform(0.88, 1.0)
            points.append((c + math.cos(ang) * rad, c + math.sin(ang) * rad))

        pygame.draw.polygon(surf, (135, 138, 145), points)
        pygame.draw.polygon(surf, (85, 88, 95), points, 2)

        for cx, cy, cr in [(-12, -10, 9), (14, -6, 7), (-4, 15, 10), (10, 12, 6), (-18, 6, 5)]:
            pygame.draw.circle(surf, (95, 98, 105), (c + cx, c + cy), cr)
            pygame.draw.circle(surf, (165, 168, 175), (c + cx + 1, c + cy + 1), cr - 2, 1)
        return surf

    def _create_missile(self) -> pygame.Surface:
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 120, 40, 140), (8, 8), 7)
        pygame.draw.circle(surf, (255, 240, 160), (8, 8), 4)
        return surf

    def _create_explosion_tileset(self) -> List[pygame.Surface]:
        tiles: List[pygame.Surface] = []
        size = 110
        c = size // 2
        for i in range(config.EXPLOSION_FRAMES):
            tile = pygame.Surface((size, size), pygame.SRCALPHA)
            progress = i / config.EXPLOSION_FRAMES
            outer_r = int(12 + math.sin(progress * math.pi) * 42)
            alpha = int((1.0 - progress) * 240)

            pygame.draw.circle(tile, (220, 60, 20, alpha), (c, c), outer_r)
            pygame.draw.circle(tile, (255, 160, 40, alpha), (c, c), int(outer_r * 0.7))
            pygame.draw.circle(tile, (255, 245, 180, alpha), (c, c), int(outer_r * 0.38))
            tiles.append(tile)
        return tiles

    def _create_splash(self) -> pygame.Surface:
        w, h = config.SPLASH_WIDTH, config.SPLASH_HEIGHT
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((45, 35, 95, 185))
        pygame.draw.rect(surf, config.SPLASH_BORDER_COLOR, (0, 0, w, h), width=3)

        title_font = pygame.font.SysFont("Arial", 54, bold=True)
        sub_font = pygame.font.SysFont("Arial", 22, bold=True)

        shadow = title_font.render("RiceRocks", True, (30, 20, 60))
        title = title_font.render("RiceRocks", True, (240, 240, 255))
        subtitle = sub_font.render("CLICK TO START", True, (255, 255, 255))

        surf.blit(shadow, shadow.get_rect(center=(w // 2 + 3, h // 2 - 22)))
        surf.blit(title, title.get_rect(center=(w // 2, h // 2 - 25)))
        surf.blit(subtitle, subtitle.get_rect(center=(w // 2, h // 2 + 45)))
        return surf
