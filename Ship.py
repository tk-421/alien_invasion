import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ Representation of the player ship"""

    def __init__(self, ai_settings, screen):
        """ Initialize the ship and its starting poisition"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the botton center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store decimal value of ship's center
        self.center = float(self.rect.centerx)

        # Movement Flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update ships position based on movement flag """
        # Update ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect from self.center
        self.rect.centerx = self.center

    def center_ship(self):
        """ Center the ship on the screen """
        self.center = self.screen_rect.centerx
