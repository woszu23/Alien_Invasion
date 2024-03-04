# settings
class Settings:
    def __init__(self):
        # inicjalizacja ustawień gry
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 120, 0)

        # ustawienie dotyczące pocisku
        self.bullet_speed = 2.0
        self.ships_limit = 3
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 5

        # ustawienie dotyczące poruszania się obcego
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 oznacza kierunek w prawo, -1 oznacza kierunek w lewo

        # łatwa zmiana szybkości gry
        self.speedup_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Inicjalizacja ustawień, które ulegają zmianie w trakcie gry'''
        self.ship_speed = 1.8
        self.bullet_speed = 3.0
        self.alien_speed = 1.5
        self.fleet_direction = -1  # 1 oznacza kierunek w prawo, -1 oznacza kierunek w lewo

        #punktacja za zestrzelenie obcego
        self.alien_points = 50

    def increase_speed(self):
        '''Zmiana dotycząca ustawień szybkości'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
