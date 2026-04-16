import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import random
import constants as c


class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.image = map_image
        self.level_data = data
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        # Look through data to extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "GrassAndDirt":
                self.tile_map = layer["data"]
            elif layer["name"] == "Object Layer 1":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]

                    for point in waypoint_data:
                        temp_x = obj["x"] + point["x"]
                        temp_y = obj["y"] + point["y"]
                        self.waypoints.append((temp_x, temp_y))

    def process_waypoints(self, data):
        # Iterate through waypoints to extract individual sets of x and y coords
        for point in data:
            temp_x = point.get("x")  # Extract the 'X' value temporarily
            temp_y = point.get("y")  # Extract the 'y' value temporarily
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        # Randomize list to shuffle enemies
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_level(self):
        # reset enemy variables
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
