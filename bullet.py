import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''klasa do zarządzania pociskami'''

    def __init__(self, ai_game):
        '''utworzenie obiektu pocisku w aktualnym położeniu statku'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        '''utworzenie prostokąta pocisku i zdefiniowanie dla niego odpowiedniego miejsca'''
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        '''polozenie pocisku za pomocą wartości zmiennoprzecinkowej float'''
        self.y = float(self.rect.y)

    def update(self):
        '''poruszanie pocisku po ekranie'''
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        '''wyswietlanie pocisku na ekranie'''
        pygame.draw.rect(self.screen, self.color, self.rect)
