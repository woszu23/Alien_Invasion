import pygame.font

class Scoreboard:
    '''klasa przeznacozna do inforamcji punktacji gry'''

    def __init__(self, screen, stats, settings):
        """inicjalizacja atrybutów dotyczacych punktacji"""
        self.screen = screen

        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Ustawienie czcionki dla informacji dotyczącej punktacji
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Przygotowanie obrazów z punktacją
        self.prep_score()
        self.prep_high_score()
        self.prep_level()


    def prep_score(self):
        '''przekształcenie punktacji na wygenerowany obraz'''
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Wyswietlanie punktacji w prawym gornym rogu
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''wyswietlanie punktacji na ekranie'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)


    def prep_high_score(self):
        # konwersja najlepszego wyniku na wygenerowany obraz
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.bg_color)

        # wyswietlanie najlepszego wyniku w grze na srodku ekranu
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """sprawdzenie czy mamy najlepszy wynik dotad osiagniety w grze"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        '''konwersja numeru poziomu na obraz'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                                            self.settings.bg_color)

        # numer lvl jest wyswietlany pod punktacja
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

