import pygame
import uuid
import requests
from .base import BaseScreen
from components.button import Button
from globalvars import HEIGHT, WIDTH

class GameOverScreen(BaseScreen):
    def __init__(self, window, final_score) -> None:
        super().__init__(window)
        self.final_score = final_score
        image = pygame.image.load("images/game_over.png").convert_alpha()
        self.image = pygame.transform.scale(image, (WIDTH // 1.6, HEIGHT // 3.6))
        self.retry = Button(pygame.image.load("images/retry.png").convert_alpha(), WIDTH // 4, HEIGHT // 1.8, 0.66)
        self.exit = Button(pygame.image.load("images/red_exit.png").convert_alpha(), WIDTH // 1.92, HEIGHT // 1.8, 0.64)
        self.score_recorded = False
        
    def draw(self):
        score_font = pygame.font.Font("fonts/minecraft.ttf", 50)
        self.score_text_surface = score_font.render(f"Your score: {self.final_score}", False, "Brown")

        self.window.blit(self.image, (180, HEIGHT // 6.75))
        self.window.blit(self.score_text_surface, (330, 430))
        self.retry.draw(self.window)
        self.exit.draw(self.window)

        # If score has not been recorded yet
        if self.score_recorded == False:
            self.score_recorded = True # Score has been recorded
            self.upload_score() # Upload the score

    def manage_event(self, event):
        if self.retry.draw(self.window):
            button_sound = pygame.mixer.Sound("audio/button-click.mp3")
            button_sound.set_volume(0.3)
            button_sound.play()
            self.final_score = 0
            self.next_screen = "game"
            self.running = False
        if self.exit.draw(self.window):
            self.running = False

    def upload_score(self):
        """Method to get the score object and posts it to url
        """
        flask_url = "http://127.0.0.1:5000/add"
        id = str(uuid.uuid4())

        game = {
            "id": id,
            "score": self.final_score
        }

        requests.post(flask_url, game)

    def update(self):
        pass