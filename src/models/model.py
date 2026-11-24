import random
from typing import List
import pygame
from src import config


class Player:

    def __init__(self) -> None:
        self.rect = pygame.Rect(
            config.SCREEN_WIDTH // 2 - config.PLAYER_WIDTH // 2,
            config.SCREEN_HEIGHT - config.PLAYER_HEIGHT - 25,
            config.PLAYER_WIDTH,
            config.PLAYER_HEIGHT,
        )
        self.speed = config.PLAYER_SPEED

    def move(self, direction: int) -> None:
        self.rect.x += int(direction * self.speed)
        self.rect.x = max(
            0, min(config.SCREEN_WIDTH - self.rect.width, self.rect.x)
        )


class Bullet:

    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(
            x - config.BULLET_WIDTH // 2,
            y - config.BULLET_HEIGHT,
            config.BULLET_WIDTH,
            config.BULLET_HEIGHT,
        )
        self.speed = config.BULLET_SPEED

    def update(self) -> None:
        self.rect.y -= int(self.speed)


class Asteroid:

    def __init__(self) -> None:
        x = random.randint(0, config.SCREEN_WIDTH - config.ASTEROID_SIZE)
        self.rect = pygame.Rect(
            x,
            -config.ASTEROID_SIZE,
            config.ASTEROID_SIZE,
            config.ASTEROID_SIZE,
        )
        self.speed = random.uniform(
            config.ASTEROID_MIN_SPEED, config.ASTEROID_MAX_SPEED
        )

    def update(self) -> None:
        self.rect.y += int(self.speed)


class GameModel:

    def __init__(self) -> None:
        self.player: Player
        self.bullets: List[Bullet] = []
        self.asteroids: List[Asteroid] = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.last_spawn_time = 0
        self.reset()

    def reset(self) -> None:
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.last_spawn_time = pygame.time.get_ticks()

    def shoot(self) -> None:
        if not self.game_over:
            self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.top))

    def update(self, move_direction: int, current_time_ms: int) -> None:
        if self.game_over:
            return

        self.player.move(move_direction)

        if current_time_ms - self.last_spawn_time >= config.SPAWN_INTERVAL_MS:
            self.asteroids.append(Asteroid())
            self.last_spawn_time = current_time_ms

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids[:]:
            asteroid.update()
            if asteroid.rect.top > config.SCREEN_HEIGHT:
                self.asteroids.remove(asteroid)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                continue

            if asteroid.rect.colliderect(self.player.rect):
                self.asteroids.remove(asteroid)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                continue

            for bullet in self.bullets[:]:
                if asteroid.rect.colliderect(bullet.rect):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.score += 10
                    break
