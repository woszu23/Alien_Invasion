import  pygame


class Ship():
    '''zarzadzanie statkiem kosmicznym'''

    def __init__(self, ai_game):
        '''inicjalizacja statku i jego polozenie'''



        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        '''wczytywanie obrazu statku'''
        self.image = pygame.image.load("images/ship.bmp")
        self.image = pygame.transform.scale(self.image, (80, 80))  # zmniejszenie/zwiekszanie obiektu
        self.rect = self.image.get_rect()
        '''kazdy nowy statek pojawia sie na dole ekranu'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False  # opcje wskazujace na poruszanie sie obiektu
    def update(self):
        '''uaktualnienie statku na podstawie jego ruchu'''
        if self.moving_right and self.rect.right < self.screen_rect.right:    #zatrzymuje sie koncu ekranu
            self.rect.x += 1
        if self.moving_left  and self.rect.left > 0:
            self.rect.x -= 1   # statek porusza sie z szybkoscia jendego pixela




    def blitme(self):
        '''wyswietlanie statku w aktulanym polozeniu'''
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        '''umieszczenie statku na srodku przy dolnej krawedzi ekranu'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)