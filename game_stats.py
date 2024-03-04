class GameStats:
    '''moonitorowanie danych statycznych w grze'''
    def __init__(self, ai_game):
        #inicjalizacja danych statycznych
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        #najlepszy wynik nigdy nie powinien zostać wyzerowany
        self.high_score = 0

    def reset_stats(self):
        '''inicjalizacja danych ktore moga sie zmieniac w grze'''
        self.ship_left = self.settings.ships_limit
        self.score = 0
        self.level = 1
