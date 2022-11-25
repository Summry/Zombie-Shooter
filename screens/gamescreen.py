import pygame
import random
from .base import BaseScreen
from components.player import Player
from components.zombie import Zombie
from components.bullet import Bullet

class GameScreen(BaseScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Create the player
        self.player = Player(480, 350, 0.2, speed=5)
        self.move_left = False
        self.move_right = False
        self.shoot = False

        # Create a zombie
        # self.zombie = Zombie(300, 300, speed=0)

        # Put all sprites in the group
        self.player_sprite = pygame.sprite.Group()
        self.player_sprite.add(self.player)

        text_font = pygame.font.SysFont("verdana", 50)
        self.score = 0
        self.text_surface = text_font.render(f"Score: {self.score}", False, "Black")

    def draw(self):
        # self.bullet_group.draw(self.window)
        self.window.blit(self.text_surface, (10, 480))
        self.player.update()

        if self.player.is_alive:
            # Shoot bullets
            if self.shoot:
                self.player.shoot()
            if self.player.in_the_air:
                # Jump animation
                self.player.update_action(2)
            elif self.move_left or self.move_right:
                # Run animation
                self.player.update_action(1)
            else:
                # Stand animation
                self.player.update_action(0)

            self.player.move(self.move_left, self.move_right)
        self.player.draw(self.window)
        # self.zombie.draw(self.window)

    def update(self):
        self.player_sprite.update()
        
    def manage_event(self, event):
        if event.type == pygame.KEYDOWN:
            # If player presses left or right arrows
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_l:
                self.shoot = True
            if event.key == pygame.K_SPACE and self.player.is_alive:
                self.player.jump = True
    

        if event.type == pygame.KEYUP:
            # If player presses left or right arrows
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_l:
                self.shoot = False