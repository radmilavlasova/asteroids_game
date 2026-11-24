import math
import random
from typing import List, Tuple
from src import config


class SpaceObject:

    def __init__(
        self,
        pos: List[float],
        vel: List[float],
        angle: float,
        angle_vel: float,
        radius: float,
    ) -> None:
        self.pos = list(pos)
        self.vel = list(vel)
        self.angle = angle
        self.angle_vel = angle_vel
        self.radius = radius

    def update(self) -> None:
        self.angle = (self.angle + self.angle_vel) % 360
        self.pos[0] = (self.pos[0] + self.vel[0]) % config.SCREEN_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % config.SCREEN_HEIGHT

    def collides_with(self, other: "SpaceObject") -> bool:
        dist = math.hypot(self.pos[0] - other.pos[0], self.pos[1] - other.pos[1])
        return dist < (self.radius + other.radius)


class Ship(SpaceObject):

    def __init__(self, pos: Tuple[float, float]) -> None:
        super().__init__(list(pos), [0.0, 0.0], 0.0, 0.0, config.SHIP_RADIUS)
        self.thrust = False

    def reset_to_center(self) -> None:
        self.pos = [config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0]
        self.vel = [0.0, 0.0]
        self.angle = 0.0
        self.thrust = False

    def get_forward_vector(self) -> Tuple[float, float]:
        rad = math.radians(self.angle)
        return math.cos(rad), math.sin(rad)

    def update(self) -> None:
        if self.thrust:
            fx, fy = self.get_forward_vector()
            self.vel[0] += fx * config.SHIP_THRUST
            self.vel[1] += fy * config.SHIP_THRUST

        self.vel[0] *= config.SHIP_FRICTION
        self.vel[1] *= config.SHIP_FRICTION

        if math.hypot(self.vel[0], self.vel[1]) < 0.02:
            self.vel = [0.0, 0.0]

        super().update()

    def shoot(self) -> "Missile":
        fx, fy = self.get_forward_vector()
        nose_x = self.pos[0] + fx * self.radius
        nose_y = self.pos[1] + fy * self.radius
        vel_x = self.vel[0] + fx * config.MISSILE_SPEED
        vel_y = self.vel[1] + fy * config.MISSILE_SPEED
        return Missile([nose_x, nose_y], [vel_x, vel_y], self.angle)


class Asteroid(SpaceObject):

    def __init__(self, pos: List[float], vel: List[float], angle_vel: float) -> None:
        super().__init__(
            pos, vel, random.uniform(0, 360), angle_vel, config.ASTEROID_RADIUS
        )


class Missile(SpaceObject):
    def __init__(self, pos: List[float], vel: List[float], angle: float) -> None:
        super().__init__(pos, vel, angle, 0.0, config.MISSILE_RADIUS)
        self.age = 0

    def update(self) -> bool:
        super().update()
        self.age += 1
        return self.age < config.MISSILE_LIFESPAN


class Explosion:

    def __init__(self, pos: List[float]) -> None:
        self.pos = list(pos)
        self.frame = 0

    def update(self) -> bool:
        self.frame += 1
        return self.frame < config.EXPLOSION_FRAMES


class GameModel:

    def __init__(self) -> None:
        self.lives = 3
        self.score = 0
        self.in_play = False
        self.debris_offset = 0.0
        self.last_spawn_time = 0
        self.ship = Ship((config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0))
        self.asteroids: List[Asteroid] = []
        self.missiles: List[Missile] = []
        self.explosions: List[Explosion] = []

    def start_game(self) -> None:
        self.lives = 3
        self.score = 0
        self.in_play = True
        self.ship.reset_to_center()
        self.asteroids.clear()
        self.missiles.clear()
        self.explosions.clear()
        self.last_spawn_time = 0

    def spawn_asteroid(self) -> None:
        if len(self.asteroids) >= config.MAX_ASTEROIDS:
            return

        for _ in range(20):
            x = random.uniform(0, config.SCREEN_WIDTH)
            y = random.uniform(0, config.SCREEN_HEIGHT)
            if math.hypot(x - self.ship.pos[0], y - self.ship.pos[1]) > config.SAFE_SPAWN_DISTANCE:
                speed = random.uniform(
                    config.ASTEROID_MIN_SPEED, config.ASTEROID_MAX_SPEED
                )
                direction = random.uniform(0, 2 * math.pi)
                vel = [math.cos(direction) * speed, math.sin(direction) * speed]
                spin = random.uniform(-config.ASTEROID_MAX_SPIN, config.ASTEROID_MAX_SPIN)
                self.asteroids.append(Asteroid([x, y], vel, spin))
                break

    def fire_missile(self) -> None:
        if self.in_play:
            self.missiles.append(self.ship.shoot())

    def update(self, turn_dir: int, thrusting: bool, current_time_ms: int) -> None:
        self.debris_offset = (
            self.debris_offset - config.DEBRIS_SCROLL_SPEED
        ) % config.SCREEN_WIDTH

        self.explosions = [exp for exp in self.explosions if exp.update()]

        if not self.in_play:
            return

        if current_time_ms - self.last_spawn_time >= config.ASTEROID_SPAWN_MS:
            self.spawn_asteroid()
            self.last_spawn_time = current_time_ms

        self.ship.angle_vel = turn_dir * config.SHIP_TURN_SPEED
        self.ship.thrust = thrusting
        self.ship.update()

        self.missiles = [m for m in self.missiles if m.update()]

        for asteroid in self.asteroids:
            asteroid.update()

        self._check_collisions()

    def _check_collisions(self) -> None:
        for missile in self.missiles[:]:
            for asteroid in self.asteroids[:]:
                if missile.collides_with(asteroid):
                    self.explosions.append(Explosion(asteroid.pos))
                    self.missiles.remove(missile)
                    self.asteroids.remove(asteroid)
                    self.score += 1
                    break

        for asteroid in self.asteroids[:]:
            if self.ship.collides_with(asteroid):
                self.explosions.append(Explosion(asteroid.pos))
                self.asteroids.remove(asteroid)
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.in_play = False
                    self.asteroids.clear()
                    self.missiles.clear()
                else:
                    self.ship.reset_to_center()
                break

