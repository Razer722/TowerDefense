import pygame as pg
import constants as c
import math
from turret_data import TURRET_DATA

# This is for using spritesheets!
'''    def load1_images(self, sprite_sheet):
        # Extract images from spritesheet
        size = sprite_sheet.get_height()  # Assuming frames are square
        steps = sprite_sheet.get_width() // size
        temp_list = []
        # Use c.ANIMATION_STEPS (which is now 5) to loop
        for x in range(steps):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            temp_list.append(temp_img)
        return temp_list
'''


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx, turret_type):
        pg.sprite.Sprite.__init__(self)
        self.shot_fx = shot_fx
        self.turret_type = turret_type
        self.sprite_sheets = sprite_sheets  # This is your list of level images

        self.upgrade_level = 1
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # 1. Get stats
        stats = TURRET_DATA[self.turret_type][self.upgrade_level - 1]
        self.range = stats.get("range")
        self.cooldown = stats.get("cooldown")
        self.total_cost = stats.get("cost")  # For the refund logic!

        # 2. Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x * c.TILE_SIZE) + c.TILE_SIZE // 2
        self.y = (self.tile_y * c.TILE_SIZE) + c.TILE_SIZE // 2

        # 3. Setup the Image (Static version)
        self.angle = 90
        # Grab the image for the current level (no [0] needed anymore)
        self.original_image = self.sprite_sheets[self.upgrade_level - 1]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # 4. Range circle setup
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        def load_images(self, sprite_sheet):
            # Since we aren't using sheets for animation anymore,
            # we just take the first frame (or the whole image if it's just one turret)
            # Since we are now passing a single static image, we just return it
            # No need to use .subsurface() anymore!
            # size = sprite_sheet.get_height()
            # img = sprite_sheet.subsurface(0, 0, size, size)
            return sprite_sheet

    def update(self, enemy_group, world):
        if self.target:
            # Update angle to follow the moving target
            x_dist = self.target.pos[0] - self.x
            y_dist = self.target.pos[1] - self.y
            self.angle = math.degrees(math.atan2(-y_dist, x_dist))

            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # Check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    # Calculate angle to target
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # Damage enemy
                    self.target.health -= c.DAMAGE
                    # Play sound effect
                    # self.shot_fx.play()
                    break  # Target the first enemy found in range

    def play_animation(self, surface):
        # Update image
        self.original_image = self.animation_list[self.frame_index]
        # Check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None
        if pg.time.get_ticks() - self.last_shot < 100:  # Show flash for 100ms
            # Draw a small yellow circle or a 'spark' image at the turret's nozzle
            flash_pos = (self.x + math.cos(math.radians(-self.angle)) * 20,
                         self.y + math.sin(math.radians(-self.angle)) * 20)
            pg.draw.circle(surface, "yellow", flash_pos, 5)

    def upgrade(self):
        self.upgrade_level += 1
        # Pull stats for the new level based on type
        stats = TURRET_DATA[self.turret_type][self.upgrade_level - 1]
        self.range = stats.get("range")
        self.cooldown = stats.get("cooldown")
        # Upgrade turret image (visuals)
        # Instead of calling load_images, just grab the image directly from the list
        self.original_image = self.sprite_sheets[self.upgrade_level - 1]
        # --- FIX ENDS HERE ---

        # Add the upgrade cost to the total every time you level up
        self.total_cost += c.UPGRADE_COST

        # upgrade range (increase circle size)
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        # Rotate the original image based on the current angle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(self.image, self.rect)

        if self.selected:
            surface.blit(self.range_image, self.range_rect)
