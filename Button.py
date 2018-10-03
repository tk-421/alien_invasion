import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """ Initialize button object """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set dimensions and properties of button
        self.width, self.height = 200, 50
        self.button_color = (70, 140, 220)
        self.text_color = (50, 180, 90)
        self.font = pygame.font.SysFont(None, 48)

        # Build button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Button message, should just be prepped once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn msg into a rendered image and center text on screen """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw a blank button and then draw message """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
