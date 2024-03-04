import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''klasa przedstawiajaca obcego'''

    def __init__(self,ai_game):
        '''inicjalizacja obcego i zdefiniowanie jego polozenia na ekranie'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings


        #wczytanie obrazu obcego i zdefiniowanie jego atrybutu rect
        self.image = pygame.image.load('images/Alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        #umieszczenie obcego w poblizu lewego gornego ekranu
        self.rect.x = self.rect.width
        self.rect.y= self.rect.height

        #przechowywanie dokladnegoi poziomego polozenia obcego
        self.x = float(self.rect.x)


    def check_edges(self):
        '''zwraca wartość True, jeśli obcy znajduje się przy krawędzi'''
        self.screen_rect = self.screen.get_rect()
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        '''przesuniecie obcego w prawo'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x