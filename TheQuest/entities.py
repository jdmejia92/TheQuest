import pygame as pg

class Ship(pg.sprite.Sprite):
    def __init__(self, pantalla, centrox, centroy):
        super().__init__()
        self.pantalla = pantalla
        self.x = x
        self.y = y
        self.speedy = 5

    def movement(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_UP]:
            self.rect.y -= self.speedy
        if teclas[pg.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.right >= self.pantalla.get_height():
            self.rect.right = self.pantalla.get_height()
