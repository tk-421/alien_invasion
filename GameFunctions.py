import sys
import pygame
import time

from Bullet import Bullet
from Alien import Alien
from Ship import Ship

class GameFunctions():

    def check_events(self, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
        """ Respond to ingame key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                    aliens, bullets, mouse_x, mouse_y)

    def check_keydown_events(self, event, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Respond to key presses """
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self.start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

    def check_keyup_events(self, event, ship):
        """ Respond to key releases """
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


    def update_screen(self, ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
        """ Update images on screen and flip to the new screen"""
        # Redraw screen on each pass
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)

        # Redraw all bullets behind ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        # Draw the score information
        sb.show_score()

        # Draw play button if game is inactive
        if not stats.game_active:
            play_button.draw_button()

        # Make most recently drawn screen visible
        pygame.display.flip()

    def update_bullets(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Update position of active bullets and clear out old bullets """
        # Update bullet position
        bullets.update()

        # Get rid of bullets which have disappeared
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        # Check for any bullets that have hit aliens
        # If so, remove the bullet and alien
        self.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

    def check_bullet_alien_collisions(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Respond to bullet-alien collisions """
        # Remove any bullets and aliens which have collided
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                stats.score += ai_settings.alien_points * len(aliens)
                sb.prep_score()
            self.check_high_score(stats, sb)

        if len(aliens) == 0:
            # Destroy existing bullets, speed up game and create a new fleet
            # If entire fleet is destroyed, start new level
            bullets.empty()
            ai_settings.increase_speed()

            # Increase level
            stats.level += 1
            sb.prep_level()

            self.create_fleet(ai_settings, screen, ship, aliens)

    def fire_bullet(self, ai_settings, screen, ship, bullets):
        """ Fires a bullet if the limit is not yet reached """
        if len(bullets) < ai_settings.max_bullets:
            # Create a new bullet and add it to the bullets group
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

    def get_number_aliens(self, ai_settings, alien_width):
        """ Determine number of aliens that fit in a row """
        available_space_x = ai_settings.screen_width - 2 * alien_width
        num_aliens_x = int(available_space_x / (2 * alien_width))
        return num_aliens_x

    def create_alien(self, ai_settings, screen, aliens, alien_number, row_number):
        """ Create alien and place it in a row """
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)

    def create_fleet(self, ai_settings, screen, ship, aliens):
        """ Create a full fleet of aliens """
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(ai_settings, screen)
        num_aliens_x = self.get_number_aliens(ai_settings, alien.rect.width)
        num_aliens_y = self.get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

        # Create first row
        for row_number in range(num_aliens_y):
            for alien_number in range(num_aliens_x):
                self.create_alien(ai_settings, screen, aliens, alien_number, row_number)

    def get_number_rows(self, ai_settings, ship_height, alien_height):
        """ Determine number of rows of aliens that fit on the screen """
        available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
        num_rows = int(available_space_y / (2 * alien_height))
        return num_rows

    def update_aliens(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Check if fleet is at an edge, then update position of all aliens in fleet """
        self.check_fleet_edges(ai_settings, aliens)
        aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(ship, aliens):
            self.ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # Look for aliens hitting the bottom of the screen
        self.check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

    def check_fleet_edges(self, ai_settings, aliens):
        """ Check if any aliens have reached screen edge and respond appropriately """
        for alien in aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction(ai_settings, aliens)
                break

    def change_fleet_direction(self, ai_settings, aliens):
        """ Drop the entire fleet and change direction """
        for alien in aliens.sprites():
            alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1

    def ship_hit(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Respond to ship being hit by aliens """

        if stats.ships_left > 0:
            # Decrement ships left
            stats.ships_left -= 1

            #Update scoreboard
            sb.prep_ships()

            # Empty the list of aliens and bullets
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center the ship
            self.create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

            # Pause game for a moment
            time.sleep(5)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Check to see if any aliens have hit the bottom of the screen """
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this same as if a ship got hit
                self.ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
                break

    def check_play_button(self, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        """ Start a new game when the player clicks Play """
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Reset the game speed settings
            ai_settings.initialize_dynamic_settings()
            # Start the game
            self.start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

    def start_game(self, ai_settings, screen, stats, sb, ship, aliens, bullets):
        """ Start the game """
        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset Stats
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center ship
        self.create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    def check_high_score(self, stats, sb):
        """ Check to see if there's a new high score """
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()
