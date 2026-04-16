import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 90
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        # Define Target Waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Enemy has reached the end of the path
            self.kill()
            world.health -= 1
            world.missed_enemies += 1
        # Calculate Distance to Target
        dist = self.movement.length()
        # Check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * self.speed * dist

            self.target_waypoint += 1

    def rotate(self):
        if self.target_waypoint < len(self.waypoints):
            dist = self.target - self.pos
            self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
            self.angle += -90  # your offset

            # Rotate image & update rectangle
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            # Check if the enemy alive is the 'slimer' type (that slows down turrets)
            if hasattr(self, 'type') and self.type == "slimer":
                self.apply_slow_debuff(world)

            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

    def apply_slow_debuff(self, world):
        # Needs access to turret_group
        for turret in world.turret_group:
            # Calculate distance to turret
            x_dist = turret.x - self.pos[0]
            y_dist = turret.y - self.pos[1]
            dist = math.sqrt(x_dist**2 + y_dist**2)

            if dist < 150:  # Splash radius of the slow effect
                turret.cooldown *= 2
