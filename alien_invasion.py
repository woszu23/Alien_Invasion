"""W grze alien invasion gracz kontorluje statek kosmiczny wyswietlany na dole ekranu.
Gracz moze poruszac statkiem w lewa i prawa strone oraz strzelać.
Zadaniem gracza jest zestrzeliwanie obcych, ktorzy przyspieszaja z kazda nastepna runda
Gracz posiada 3 zycia"""

import pygame.font
import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button






class AlienInvasion:
    '''ogolna klasa do zarzadzania zasobami i sposobem dzialania gry'''
    def __init__(self):
        '''inicjalizacja gry oraz jej zasobow'''
        pygame.init()
        self.settings = Settings()

        # Ustawienie rozmiaru ekranu gry
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height
        ))
        pygame.display.set_caption("Alien Invasion")

        # Utworzenie egzemplarza przechwywającego dane statystyczne gry
        self.stats = GameStats(self)
        #utowrzenie egzmeplarza do przechowywania danych
        self.sb = Scoreboard(self.screen,self.stats, self.settings)

        # Utworzenie statku kosmicznego
        self.ship = Ship(self)
        self.bg_color = (0, 120, 0)

        # Utworzenie grupy pocisków i obcych
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Utworzenie floty obcych
        self._create_fleet()

        # Utworzenie przycisku GRA
        self.play_button = Button(self, "INWAZJA OBCYCH!")

        self.button_clicked = False




    def run_game(self):
        while not self.stats.game_active:
            self._check_events()
            self._update_screen()
        '''Rozpoczecie petli glownej gry'''
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_screen()
            self._update_aliens()

            self._check_bullet_alien_collisions()  # Wywołanie metody, po aktualizacji pocisków i obcych

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

                    self._update_screen()
                    pygame.display.flip()







            '''usuniecie pociskow, ktore znajduja sie poza ekranem'''
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)


            self._update_screen()
            pygame.display.flip()


    def _check_events(self):
        '''reakcja na klawiaturę i mysz'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.button_clicked = False  # Resetuj flagę po naciśnięciu spacji

    def _check_play_button(self, mouse_pos):
        '''rozpoczęcie gry po kliknięciu Inwazja Obcych'''
        if self.play_button.rect.collidepoint(mouse_pos):
            if not self.stats.game_active:
                # wyzerowanie ustawien dotyczacuch gry
                self.settings.initialize_dynamic_settings()
                self.stats.reset_stats()  # wyzerowanie danych statystycznych gry
                self.stats.score = 0 # reset punktacji
                self.stats.game_active = True
                self.sb.prep_score()
                self.sb.prep_level()

                # usunięcie zawartości list aliens i bullets
                self.aliens.empty()
                self.bullets.empty()

                # utworzenie nowej floty i statku
                self._create_fleet()
                self.ship.center_ship()

            # ukrycie kursora myszy
            pygame.mouse.set_visible(False)

            # ustawienie flagi button_click na True po nacisnieciu przycisku
            self.button_clicked = True
    def _check_keydown_events(self, event):
        '''reakcja na naciśnięcie klawisza'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:     # klawisz Q powoduje wyjscie z gry
            self._quit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _quit_game(self):
        pygame.quit()
        sys.exit()



    def _check_keyup_events(self, event):
        '''reakcja na zwolnienie klawisza'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        '''utowrzenie nowego pocisku i dodanie go do grupy pociskow'''
        if len(self.bullets) < self.settings.bullet_allowed:

           new_bullet = Bullet(self)
           self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''uaktualnienie polozenia pociskow i usuniecie tych niewidocznych'''
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #sprawdznie czy pocisk trafil obcego, jesli tak to znika
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # pozbycie sie istniejacych pociskow i utworzenie nowej floty
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        '''uaktulanieie polozenia wsztkich obcych we flocie'''
        self._check_fleet_edges()  #sprawdzenie czy flota znajduje sie przyu krawedzi
        self.aliens.update()
        #wykrywanie kolizji miedzy obcym a statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):

            self._ship_hit()

        #wyszykiuwanie obcych docierajacy do dolu ekranu
        self._check_aliens_bottom()



    def _ship_hit(self):
        '''reakcja na uderzenie obcego w statek'''
        # Zmniejszenie wartości przechwywanej w ship_left, jeśli są jeszcze jakieś życia
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1

            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()


            # Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

            # Pauza
            sleep(2.0)
        else:
            self.stats.game_active = False
            self.stats.score = 0
            pygame.mouse.set_visible(True)




    def _create_fleet(self):
        '''utworzenie pelenj floty obcych'''
        alien = Alien(self)   #dodanie obcego
        '''utowrzenie obcego i ustalenie liczby obcych oraz odleglosc miedzy nimi'''
        alien_width, alien_hight = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width -(2* alien_width)
        number_aliens_x = available_space_x // (2* alien_width)
        #ustalenie ile rzedow obcych zmiesci sie na ekranie
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3* alien_hight) - ship_height)
        number_rows = available_space_y // (2* alien_hight)
        #utworzenie pelenj floty obcych
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):

                self._create_alien(alien_number , row_number)


    def _create_alien(self, alien_number, row_number):
        #utowrzenie obego i umieszenie go w rzedzie
        alien = Alien(self)
        alien.width, alien.hight = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width +2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 *alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''odpowiednia rekacja jak obcy dodtrze do krawedzi ekranu'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''przesuniecie calej floty w dol i zmiana kierunku w ktorym sie porusza'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        '''uaktualnienie obrazu i przejście do nowego ekranu'''
        self.screen.fill(self.bg_color)
        self.ship.update()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #wyswietlanie informacji o punktacji
        self.sb.show_score()
        #wyswietlanie przycisku gdy gra jest nieaktywna
        if not self.stats.game_active and not self.button_clicked:
            self.play_button.draw_button()

        pygame.display.flip()


    def _check_aliens_bottom(self):
        '''sprawdzenie czy obcy dotarl do dolenj krawedzi ekranu'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
           if alien.rect.bottom >= screen_rect.bottom:
            #tak samo jak w przypadku zderzenia z obcym
            self._ship_hit()
            break



    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                # Dodawanie punktów za każde trafione obcego
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()  # Aktualizacja punktacji po trafieniu obcych
            self.sb.check_high_score()
        if not self.aliens:
            #usuniecie istniejacych przyciskow,przyspieszenie gry i utworzenie nowej floty
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #inkrementacja numeru poziomu
            self.stats.level +=1
            self.sb.prep_level()



if __name__ == '__main__':
    # utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()
