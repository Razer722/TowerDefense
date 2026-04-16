import pygame as pg


class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pg.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                # If button is a single click type, set variable 'single_click' to True
                if self.single_click:
                    self.single_click = True  # This doesn't do anything cuz it's already true
                    self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, self.rect)
        # pg.draw.rect(surface, "red", self.rect, 3)  # ---------- DEBUG

        return action
