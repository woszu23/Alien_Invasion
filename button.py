import pygame
class Button():
    def __init__(self, ai_game, msg):
        pass
        '''inicjalizacja atrybutow przycisku'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # zdefiniowanie wymiarow przycisku
        self.width, self.height = 200, 60
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # utworzenie prostokata przycisku i wysrodkowanie go
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # komiunikat wyswietlany przez przycisk
        self._prep_msg(msg)


    def _prep_msg(self,msg):
        '''umieszczanie komunikatu w wygerewowanym obrazie'''
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #wyswietlanie pustego przycisku, a nstepenie komunikatu w nim
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
