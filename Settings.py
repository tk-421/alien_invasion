class Settings():
    """ Stores all of the settings for Alien Invasion"""

    def __init__(self):
        """ Initialize the game settings """
        # screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # ship
        self.ship_limit = 3

        # bullets
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.max_bullets = 1000

        # Aliens
        self.alien_drop_speed = 10

        # Fleet
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.25

        # How quickly score scales up
        self.score_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings which change throughout the game """
        # Ship, Alien, and Bullet horizontal speed
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1.5

        # Fleet direction. 1 represents right, -1 is left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed of various game attributes """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
